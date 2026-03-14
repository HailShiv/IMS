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
        if self.city:
            return f"{self.name} ({self.city})"
        return self.name
