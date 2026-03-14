from django.urls import path
from . import views

app_name = 'transfers'

urlpatterns = [
    path('create/', views.transfer_request_create, name='create'),
    path('sent/', views.sent_requests, name='sent_requests'),
    path('received/', views.received_requests, name='received_requests'),
    path('accept/<int:pk>/', views.accept_request, name='accept_request'),
    path('reject/<int:pk>/', views.reject_request, name='reject_request'),
]

