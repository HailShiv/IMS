from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from products.models import Product, Category, ProductVariant
from .models import Cart, CartItem, Order, OrderItem

@login_required
def product_list(request):
    # Get categories for tshirts, shirts, jeans
    category_names = ['T-Shirts', 'Shirts', 'Jeans']
    categories = Category.objects.filter(name__in=category_names, is_active=True)
    products = Product.objects.filter(category__in=categories, is_active=True).prefetch_related('variants')

    # Get user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    cart_item_dict = {item.product_variant.id: item.quantity for item in cart_items}

    context = {
        'products': products,
        'cart_item_dict': cart_item_dict,
    }
    return render(request, 'online_orders/product_list.html', context)

@login_required
def add_to_cart(request, variant_id):
    if request.method == 'POST':
        variant = get_object_or_404(ProductVariant, id=variant_id)
        quantity = int(request.POST.get('quantity', 1))

        if quantity > variant.total_stock:
            messages.error(request, 'Insufficient stock available.')
            return redirect('online_orders:product_list')

        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_variant=variant,
            defaults={'quantity': quantity}
        )
        if not created:
            if cart_item.quantity + quantity > variant.total_stock:
                messages.error(request, 'Insufficient stock available.')
                return redirect('online_orders:product_list')
            cart_item.quantity += quantity
            cart_item.save()

        messages.success(request, f'Added {quantity} x {variant} to cart.')
        return redirect('online_orders:product_list')
    return redirect('online_orders:product_list')

@login_required
def update_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        action = request.POST.get('action')
        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        elif action == 'remove':
            cart_item.delete()
        return redirect('online_orders:cart')
    return redirect('online_orders:cart')

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product_variant__product').all()

    total_amount = sum(item.total_price for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
    }
    return render(request, 'online_orders/cart.html', context)

@login_required
def request_products(request):
    if request.method == 'POST':
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = cart.items.all()
        if not cart_items:
            messages.error(request, 'Your cart is empty.')
            return redirect('online_orders:cart')

        # Create order
        total_amount = sum(item.total_price for item in cart_items)
        order = Order.objects.create(
            user=request.user,
            warehouse=request.user.warehouse,
            total_amount=total_amount,
            status='pending'
        )

        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product_variant=cart_item.product_variant,
                quantity=cart_item.quantity,
                unit_price=cart_item.product_variant.product.unit_price
            )

        # Clear cart
        cart_items.delete()

        messages.success(request, f'Order #{order.id} has been placed successfully.')
        return redirect('online_orders:orders_history')
    return redirect('online_orders:cart')

@login_required
def orders_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at').prefetch_related('items__product_variant__product')
    context = {
        'orders': orders,
    }
    return render(request, 'online_orders/orders_history.html', context)
