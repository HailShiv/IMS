from django.conf import settings
from django.db import models


class Warehouse(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True, default="")
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_warehouses",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
<<<<<<< HEAD
        if self.city:
            return f"{self.name} ({self.city})"
        return self.name
=======
        return f"{self.id} - {self.name}"

class WarehouseStock(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stocks')
    product_variant = models.ForeignKey('products.ProductVariant', on_delete=models.CASCADE, related_name='warehouse_stocks')
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('warehouse', 'product_variant')

    def __str__(self):
        return f"{self.warehouse.name} - {self.product_variant} - {self.quantity}"
>>>>>>> 8ef5cc61f27ad82c7ad94cd87a50f916508c98f3
