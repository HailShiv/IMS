from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login

def index(request):
    return render(request, 'home/index.html')

def user_login(request):
    return render(request, 'home/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

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

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password1
        )
        user.save()

        # Log the user in after registration
        login(request, user)
        messages.success(request, 'Registration successful! Welcome to CoreInventory IMS.')
        return redirect('home')  # Assuming 'home' is the name for index

    return render(request, 'home/registration.html')