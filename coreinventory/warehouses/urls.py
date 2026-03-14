from django.urls import path

from . import views

app_name = 'warehouses'

urlpatterns = [
    path('', views.warehouse_list, name='list'),
    path('add/', views.warehouse_create, name='create'),
    path('edit/<int:pk>/', views.warehouse_update, name='update'),
    path('delete/<int:pk>/', views.warehouse_delete, name='delete'),
]

