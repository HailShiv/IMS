from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('logout/', views.user_logout, name='logout'),
]
