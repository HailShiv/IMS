"""
URL configuration for coreinventory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🔐 Accounts (login, users, roles)
    path('accounts/', include('accounts.urls')),

    # 🏬 Stores & Warehouses
    path('stores/', include('stores.urls')),

    # 📦 Product Catalog
    path('products/', include('products.urls')),

    # 📊 Inventory Management
    path('inventory/', include('inventory.urls')),

    # 🔄 Stock Transfers
    path('transfers/', include('transfers.urls')),

    # 💰 Sales / POS
    path('sales/', include('sales.urls')),

    # 📈 Reports & Analytics
    path('reports/', include('reports.urls')),
]

