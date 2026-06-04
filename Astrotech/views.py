from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from functools import wraps
from shop.models import Product


def register_view(request):
    """Handle user registration"""
    # Redirect already authenticated users to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        # Validation
        if not all([first_name, email, password, confirm_password]):
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'register.html', {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
            })
        
        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Please enter a valid email address.')
            return render(request, 'register.html', {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
            })
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered. Please login or use a different email.')
            return render(request, 'register.html', {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
            })
        
        # Check password length
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'register.html', {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
            })
        
        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html', {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
            })
        
        # Create user with email as username
        try:
            username = email.split('@')[0]  # Use email prefix as username
            
            # Ensure username is unique
            counter = 1
            original_username = username
            while User.objects.filter(username=username).exists():
                username = f"{original_username}{counter}"
                counter += 1
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            
            messages.success(request, 'Account created successfully! Please login to continue.')
            return redirect('login')
            
        except Exception as e:
            messages.error(request, f'An error occurred while creating your account. Please try again.')
            return render(request, 'register.html', {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
            })
    
    return render(request, 'register.html')


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


# ADMIN DECORATOR
def admin_required(view_func):
    """Decorator to check if user is admin"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login first.')
            return redirect('login')
        if not request.user.is_staff:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


# ADMIN DASHBOARD
@admin_required
def admin_dashboard_view(request):
    """Admin dashboard with overview"""
    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_admin = User.objects.filter(is_staff=True).count()
    
    context = {
        'total_users': total_users,
        'total_products': total_products,
        'total_admin': total_admin,
        'recent_users': User.objects.order_by('-date_joined')[:5],
        'recent_products': Product.objects.order_by('-created_at')[:5],
    }
    return render(request, 'admin/dashboard.html', context)


# USER MANAGEMENT
@admin_required
def admin_users_view(request):
    """List all users"""
    users = User.objects.all().order_by('-date_joined')
    context = {
        'users': users,
        'total_users': users.count(),
    }
    return render(request, 'admin/users.html', context)


@admin_required
def admin_add_user_view(request):
    """Add new user"""
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        is_staff = request.POST.get('is_staff') == 'on'
        
        # Validation
        if not all([first_name, email, password]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'admin/add_user.html')
        
        # Validate email
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Please enter a valid email address.')
            return render(request, 'admin/add_user.html')
        
        # Check if email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered.')
            return render(request, 'admin/add_user.html')
        
        # Create user
        try:
            username = email.split('@')[0]
            counter = 1
            original_username = username
            while User.objects.filter(username=username).exists():
                username = f"{original_username}{counter}"
                counter += 1
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_staff=is_staff,
            )
            messages.success(request, f'User {email} created successfully.')
            return redirect('admin_users')
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
            return render(request, 'admin/add_user.html')
    
    return render(request, 'admin/add_user.html')


@admin_required
def admin_edit_user_view(request, user_id):
    """Edit user"""
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        user.email = request.POST.get('email', '').strip()
        user.is_staff = request.POST.get('is_staff') == 'on'
        user.is_active = request.POST.get('is_active') == 'on'
        
        # Check if new email exists (for other users)
        if User.objects.filter(email=user.email).exclude(id=user_id).exists():
            messages.error(request, 'This email is already in use.')
            return render(request, 'admin/edit_user.html', {'user': user})
        
        password = request.POST.get('password', '').strip()
        if password:
            user.set_password(password)
        
        try:
            user.save()
            messages.success(request, f'User {user.email} updated successfully.')
            return redirect('admin_users')
        except Exception as e:
            messages.error(request, f'Error updating user: {str(e)}')
    
    return render(request, 'admin/edit_user.html', {'user': user})


@admin_required
def admin_delete_user_view(request, user_id):
    """Delete user"""
    user = get_object_or_404(User, id=user_id)
    
    if request.user.id == user_id:
        messages.error(request, 'You cannot delete your own account.')
        return redirect('admin_users')
    
    email = user.email
    user.delete()
    messages.success(request, f'User {email} deleted successfully.')
    return redirect('admin_users')


# PRODUCT MANAGEMENT
@admin_required
def admin_products_view(request):
    """List all products"""
    products = Product.objects.all().order_by('-created_at')
    context = {
        'products': products,
        'total_products': products.count(),
        'categories': Product._meta.get_field('category').choices
    }
    return render(request, 'admin/products.html', context)


@admin_required
def admin_add_product_view(request):
    """Add new product"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        category = request.POST.get('category', '').strip()
        price = request.POST.get('price', '')
        description = request.POST.get('description', '').strip()
        stock = request.POST.get('stock', '0')
        image_url = request.POST.get('image_url', '').strip()
        
        # Validation
        if not all([name, category, price, description, stock]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'admin/add_product.html', {
                'categories': Product._meta.get_field('category').choices
            })
        
        try:
            product = Product.objects.create(
                name=name,
                category=category,
                price=price,
                description=description,
                stock=int(stock),
                image_url=image_url if image_url else None,
                created_by=request.user,
            )
            messages.success(request, f'Product {name} created successfully.')
            return redirect('admin_products')
        except Exception as e:
            messages.error(request, f'Error creating product: {str(e)}')
            return render(request, 'admin/add_product.html', {
                'categories': Product._meta.get_field('category').choices
            })
    
    context = {
        'categories': Product._meta.get_field('category').choices
    }
    return render(request, 'admin/add_product.html', context)


@admin_required
def admin_edit_product_view(request, product_id):
    """Edit product"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product.name = request.POST.get('name', '').strip()
        product.category = request.POST.get('category', '').strip()
        product.price = request.POST.get('price', '')
        product.description = request.POST.get('description', '').strip()
        product.stock = int(request.POST.get('stock', '0'))
        image_url = request.POST.get('image_url', '').strip()
        product.image_url = image_url if image_url else None
        
        try:
            product.save()
            messages.success(request, f'Product {product.name} updated successfully.')
            return redirect('admin_products')
        except Exception as e:
            messages.error(request, f'Error updating product: {str(e)}')
    
    context = {
        'product': product,
        'categories': Product._meta.get_field('category').choices
    }
    return render(request, 'admin/edit_product.html', context)


@admin_required
def admin_delete_product_view(request, product_id):
    """Delete product"""
    product = get_object_or_404(Product, id=product_id)
    name = product.name
    product.delete()
    messages.success(request, f'Product {name} deleted successfully.')
    return redirect('admin_products')
