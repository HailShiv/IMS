from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
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

def index(request):
    if request.GET.get('logout'):
        from django.contrib.auth import logout
        logout(request)
        return redirect('login')
    warehouse_name = request.user.warehouse.name if request.user.is_authenticated else 'N/A'
    return render(request, 'home/index.html', {'warehouse_name': warehouse_name})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
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

        # Static warehouse IDs (assume they exist or create on fly if allowed)
        warehouse_id = int(warehouse_id)
        if warehouse_id not in [1,2,3]:
            messages.error(request, 'Invalid warehouse selected.')
            return redirect('register')

        role = int(role)
        if role not in [1,2]:
            messages.error(request, 'Invalid role selected.')
            return redirect('register')

        try:
            warehouse = Warehouse.objects.get(id=warehouse_id)
        except Warehouse.DoesNotExist:
            # Fallback create if not exists (for dev)
            warehouse = Warehouse.objects.create(id=warehouse_id, name=['ahmedabad','surat','vadodara'][warehouse_id-1])
            messages.warning(request, 'Warehouse created (dev mode).')

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
        return redirect('home')

    # Static warehouses and roles for dropdown
    static_warehouses = [
        {'id': 1, 'name': 'ahmedabad'},
        {'id': 2, 'name': 'surat'},
        {'id': 3, 'name': 'vadodara'},
    ]
    static_roles = [
        {'id': 1, 'name': 'Head Manager'},
        {'id': 2, 'name': 'Warehouse Manager'},
    ]
    return render(request, 'home/registration.html', {'warehouses': static_warehouses, 'roles': static_roles})
