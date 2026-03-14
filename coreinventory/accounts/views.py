from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, LogoutView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.sites.shortcuts import get_current_site
from .models import User
from warehouses.models import Warehouse

class CustomPasswordResetView(PasswordResetView):
    template_name = 'home/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = '/accounts/password_reset/done/'
    token_generator = default_token_generator

    def get_users(self, email):
        email_field_name = self.get_email_field_name()
        active_users = self.get_user_model()._default_manager.filter(**{
            '%s__iexact' % email_field_name: email
        }).exclude(is_active=False)
        return (u for u in active_users if u.has_usable_password())

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'home/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'home/password_reset_confirm.html'
    success_url = '/accounts/password_reset/complete/'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'home/password_reset_complete.html'

class CustomLogoutView(LogoutView):
    next_page = 'login'

def index(request):
    warehouse_name = 'N/A'
    if request.user.is_authenticated:
        if request.user.role == 1:
            warehouse_name = 'All Warehouses'
        else:
            try:
                warehouse_name = request.user.warehouse.name
            except:
                warehouse_name = 'N/A'
    return render(request, 'home/index.html', {'warehouse_name': warehouse_name})

@login_required
def admin_panel(request):
    warehouse_name = 'N/A'
    if request.user.is_authenticated:
        if request.user.role == 1:
            warehouse_name = 'All Warehouses'
        else:
            try:
                warehouse_name = request.user.warehouse.name
            except:
                warehouse_name = 'N/A'
    return render(request, 'home/admin_panel.html', {'warehouse_name': warehouse_name})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            if user.role == 1:
                return redirect('admin_panel')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'home/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        warehouse_id = request.POST['warehouse']
        role = request.POST['role']

        # Validation
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')

        warehouse_id = int(warehouse_id)
        try:
            warehouse = Warehouse.objects.get(id=warehouse_id)
        except Warehouse.DoesNotExist:
            messages.error(request, 'Selected warehouse does not exist.')
            return redirect('register')

        role = int(role)
        if role not in [1,2]:
            messages.error(request, 'Invalid role selected.')
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            role=role,
            warehouse=warehouse
        )

        # Log the user in after registration
        login(request, user)
        messages.success(request, 'Registration successful! Welcome to CoreInventory IMS.')
        return redirect('admin_panel')

    # Check if warehouses exist, create default if not
    warehouses = Warehouse.objects.all().order_by('id')
    if not warehouses:
        # Create a default warehouse for initial setup
        Warehouse.objects.create(id=1, name='Default Warehouse')
        warehouses = Warehouse.objects.all().order_by('id')

    roles = [
        {'id': 1, 'name': 'Head Manager'},
        {'id': 2, 'name': 'Warehouse Manager'},
    ]
    return render(request, 'home/registration.html', {'warehouses': warehouses, 'roles': roles})
