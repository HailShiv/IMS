<<<<<<< Updated upstream
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Product, Category

@login_required
def product_list(request):
    products = Product.objects.all().select_related('category')
    return render(request, 'products/product_list.html', {'products': products})

@login_required
def product_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        sku = request.POST['sku']
        unit_price = request.POST['unit_price']
        category_id = request.POST.get('category')
        
        category = Category.objects.get(id=category_id) if category_id else None
        
        Product.objects.create(
            name=name,
            sku=sku,
            unit_price=unit_price,
            description=description,
            category=category,
            cost_price=float(unit_price) * 0.8,  # Default cost = 80% unit price
            reorder_level=request.POST.get('reorder_level', 0)
        )
        messages.success(request, 'Product created successfully!')
        return redirect('products:product_list')
    
    categories = Category.objects.filter(is_active=True)
    return render(request, 'products/product_form_fixed.html', {'categories': categories, 'action': 'Add'})

@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.name = request.POST['name']
        product.sku = request.POST['sku']
        product.unit_price = float(request.POST['unit_price'])
        product.description = request.POST.get('description', '')
        category_id = request.POST.get('category')
        product.category = Category.objects.get(id=category_id) if category_id else None
        product.reorder_level = request.POST.get('reorder_level', 0)
        product.save()
        messages.success(request, 'Product updated successfully!')
        return redirect('products:product_list')
    
    categories = Category.objects.filter(is_active=True)
    return render(request, 'products/product_form_fixed.html', {
        'product': product, 
        'categories': categories, 
        'action': 'Edit'
    })

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('products:product_list')
    return render(request, 'products/confirm_delete.html', {'product': product})

@login_required
def product_toggle_active(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.is_active = not product.is_active
    product.save()
    messages.success(request, f'Product {"activated" if product.is_active else "deactivated"} successfully!')
    return redirect('products:product_list')
=======
from django.shortcuts import render
from .models import Product

def product_list(request):
    products = Product.objects.filter(is_active=True).select_related('category')[:20]  # Limit for performance
    context = {
        'products': products,
        'total_products': Product.objects.filter(is_active=True).count(),
    }
    return render(request, 'products/product_list.html', context)
>>>>>>> Stashed changes
