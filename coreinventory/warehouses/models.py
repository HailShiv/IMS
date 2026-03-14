from django.db import models
from django.utils import timezone

class Warehouse(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True, default='')
    created_at = models.DateTimeField(default=timezone.now)
    manager = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_warehouses')

    def __str__(self):
        return f"{self.id} - {self.name}"

class WarehouseStock(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stocks')
    product_variant = models.ForeignKey('products.ProductVariant', on_delete=models.CASCADE, related_name='warehouse_stocks')
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('warehouse', 'product_variant')

    def __str__(self):
        return f"{self.warehouse.name} - {self.product_variant} - {self.quantity}"
