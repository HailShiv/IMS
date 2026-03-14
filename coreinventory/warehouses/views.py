from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import WarehouseForm
from .models import Warehouse


@login_required
def warehouse_list(request):
    warehouses = Warehouse.objects.all().order_by('id')
    return render(request, 'warehouses/warehouse_list.html', {'warehouses': warehouses})


@login_required
def warehouse_create(request):
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Warehouse created successfully.')
            return redirect('warehouses:list')
    else:
        form = WarehouseForm()

    return render(request, 'warehouses/warehouse_form.html', {'form': form, 'title': 'Add Warehouse'})


@login_required
def warehouse_update(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk)
    if request.method == 'POST':
        form = WarehouseForm(request.POST, instance=warehouse)
        if form.is_valid():
            form.save()
            messages.success(request, 'Warehouse updated successfully.')
            return redirect('warehouses:list')
    else:
        form = WarehouseForm(instance=warehouse)

    return render(request, 'warehouses/warehouse_form.html', {'form': form, 'title': 'Edit Warehouse'})


@login_required
def warehouse_delete(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk)
    if request.method == 'POST':
        warehouse.delete()
        messages.success(request, 'Warehouse deleted successfully.')
        return redirect('warehouses:list')

    return render(request, 'warehouses/warehouse_confirm_delete.html', {'warehouse': warehouse})
