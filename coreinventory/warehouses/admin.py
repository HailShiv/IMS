from django.contrib import admin

from .models import Warehouse


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'manager', 'created_at')
    list_select_related = ('manager',)
    search_fields = ('name', 'city')
    list_filter = ('city',)
