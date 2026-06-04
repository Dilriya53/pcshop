"""
URL configuration for Astrotech project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView
from views import (
    login_view, register_view, dashboard_view, logout_view,
    admin_dashboard_view, admin_users_view, admin_add_user_view,
    admin_edit_user_view, admin_delete_user_view,
    admin_products_view, admin_add_product_view,
    admin_edit_product_view, admin_delete_product_view
)

urlpatterns = [
    path('admin-panel/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    
    # ADMIN ROUTES
    path('admin/', admin_dashboard_view, name='admin_dashboard'),
    path('admin/users/', admin_users_view, name='admin_users'),
    path('admin/users/add/', admin_add_user_view, name='admin_add_user'),
    path('admin/users/<int:user_id>/edit/', admin_edit_user_view, name='admin_edit_user'),
    path('admin/users/<int:user_id>/delete/', admin_delete_user_view, name='admin_delete_user'),
    path('admin/products/', admin_products_view, name='admin_products'),
    path('admin/products/add/', admin_add_product_view, name='admin_add_product'),
    path('admin/products/<int:product_id>/edit/', admin_edit_product_view, name='admin_edit_product'),
    path('admin/products/<int:product_id>/delete/', admin_delete_product_view, name='admin_delete_product'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
