from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/accounts/login/')),
    path('admin/', admin.site.urls),

    path('accounts/', include('accounts.urls')),
    path('warehouses/', include('warehouses.urls')),
    path('products/', include('products.urls')),
    path('inventory/', include('inventory.urls')),
    path('procurement/', include('procurement.urls')),
    path('transfers/', include('transfers.urls')),
    path('online_orders/', include('online_orders.urls')),
    path('analytics/', include('analytics.urls')),
]