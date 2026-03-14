from django.db import models
from django.conf import settings

class TransferRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    from_warehouse = models.ForeignKey('warehouses.Warehouse', on_delete=models.CASCADE, related_name='sent_transfers')
    to_warehouse = models.ForeignKey('warehouses.Warehouse', on_delete=models.CASCADE, related_name='received_transfers')
    product_variant = models.ForeignKey('products.ProductVariant', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Transfer {self.quantity} of {self.product_variant} from {self.from_warehouse} to {self.to_warehouse} - {self.status}"
