from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import User
from warehouses.models import Warehouse

def index(request):
    return render(request, 'home/index.html')

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

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

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
