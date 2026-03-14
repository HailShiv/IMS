from django.urls import path
from . import views

app_name = 'procurement'

urlpatterns = [
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('purchase-orders/', views.purchase_orders, name='purchase_orders'),
]

