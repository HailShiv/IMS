from django.urls import path
from . import views

app_name = 'online_orders'

urlpatterns = [
    path('product-list/', views.product_list, name='product_list'),
    path('add-to-cart/<int:variant_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('request-products/', views.request_products, name='request_products'),
    path('orders-history/', views.orders_history, name='orders_history'),
]

