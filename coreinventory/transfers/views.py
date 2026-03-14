from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import TransferRequest
from warehouses.models import Warehouse, WarehouseStock
from products.models import ProductVariant

@login_required
def transfer_request_create(request):
    if request.method == 'POST':
        to_warehouse_id = request.POST.get('to_warehouse')
        product_variant_id = request.POST.get('product_variant')
        quantity_str = request.POST.get('quantity')

        try:
            quantity = int(quantity_str)
        except ValueError:
            messages.error(request, 'Invalid quantity.')
            return redirect('transfers:create')

        from_warehouse = request.user.warehouse
        to_warehouse = get_object_or_404(Warehouse, id=to_warehouse_id)
        product_variant = get_object_or_404(ProductVariant, id=product_variant_id)

        if from_warehouse == to_warehouse:
            messages.error(request, 'Cannot transfer to the same warehouse.')
            return redirect('transfers:create')

        if quantity <= 0:
            messages.error(request, 'Quantity must be positive.')
            return redirect('transfers:create')

        # Check if sender has enough stock
        sender_stock, created = WarehouseStock.objects.get_or_create(
            warehouse=from_warehouse, product_variant=product_variant, defaults={'quantity': 0}
        )
        if sender_stock.quantity < quantity:
            messages.error(request, f'Insufficient stock. Available: {sender_stock.quantity}')
            return redirect('transfers:create')

        TransferRequest.objects.create(
            from_warehouse=from_warehouse,
            to_warehouse=to_warehouse,
            product_variant=product_variant,
            quantity=quantity,
            requested_by=request.user
        )
        messages.success(request, 'Transfer request sent successfully.')
        return redirect('transfers:sent_requests')

    warehouses = Warehouse.objects.exclude(id=request.user.warehouse.id)
    product_variants = ProductVariant.objects.filter(warehouse_stocks__warehouse=request.user.warehouse, warehouse_stocks__quantity__gt=0).distinct()
    if not product_variants:
        product_variants = ProductVariant.objects.all()
    return render(request, 'transfers/transfer_request_form.html', {
        'warehouses': warehouses,
        'product_variants': product_variants
    })

@login_required
def sent_requests(request):
    requests = TransferRequest.objects.filter(requested_by=request.user).order_by('-created_at')
    return render(request, 'transfers/sent_requests.html', {'requests': requests})

@login_required
def received_requests(request):
    requests = TransferRequest.objects.filter(to_warehouse=request.user.warehouse, status='pending').order_by('-created_at')
    return render(request, 'transfers/received_requests.html', {'requests': requests})

@login_required
def accept_request(request, pk):
    transfer = get_object_or_404(TransferRequest, pk=pk, status='pending')
    if transfer.to_warehouse != request.user.warehouse:
        messages.error(request, 'You can only accept requests for your warehouse.')
        return redirect('transfers:received_requests')

    # Update stocks
    sender_stock, created = WarehouseStock.objects.get_or_create(
        warehouse=transfer.from_warehouse, product_variant=transfer.product_variant, defaults={'quantity': 0}
    )
    receiver_stock, created = WarehouseStock.objects.get_or_create(
        warehouse=transfer.to_warehouse, product_variant=transfer.product_variant, defaults={'quantity': 0}
    )

    if sender_stock.quantity >= transfer.quantity:
        sender_stock.quantity -= transfer.quantity
        receiver_stock.quantity += transfer.quantity
        sender_stock.save()
        receiver_stock.save()

        transfer.status = 'accepted'
        transfer.accepted_at = timezone.now()
        transfer.save()
        messages.success(request, 'Transfer request accepted.')
    else:
        messages.error(request, 'Insufficient stock in sender warehouse.')

    return redirect('transfers:received_requests')

@login_required
def reject_request(request, pk):
    transfer = get_object_or_404(TransferRequest, pk=pk, status='pending')
    if transfer.to_warehouse != request.user.warehouse:
        messages.error(request, 'You can only reject requests for your warehouse.')
        return redirect('transfers:received_requests')
    transfer.status = 'rejected'
    transfer.save()
    messages.success(request, 'Transfer request rejected.')
    return redirect('transfers:received_requests')
