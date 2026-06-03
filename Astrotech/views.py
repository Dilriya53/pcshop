from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages


def login_view(request):
    """Handle user login with email and password"""
    # Redirect already authenticated users to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        
        if not email or not password:
            messages.error(request, 'Please enter both email and password.')
            return render(request, 'login.html')
        
        # Try to find user by email
        try:
            user = User.objects.get(email=email)
            # Authenticate using username with the password
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Your account is disabled.')
            else:
                messages.error(request, 'Invalid email or password. Please try again.')
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password. Please try again.')
    
    return render(request, 'login.html')


@login_required(login_url='login')
def dashboard_view(request):
    """Display user dashboard with profile"""
    context = {
        'user': request.user,
    }
    return render(request, 'dashboard.html', context)


def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')
