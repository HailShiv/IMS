from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/accounts/login/')),
    path('admin/', admin.site.urls),

    path('accounts/', include('accounts.urls')),
    path('stores/', include('stores.urls')),
    path('products/', include('products.urls')),
    path('inventory/', include('inventory.urls')),
    path('transfers/', include('transfers.urls')),
    path('sales/', include('sales.urls')),
    path('reports/', include('reports.urls')),
]