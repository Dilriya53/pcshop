from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Admin Dashboard
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),

    # User Management
    path('admin/users/', views.admin_users_view, name='admin_users'),
    path('admin/users/add/', views.admin_add_user_view, name='admin_add_user'),
    path('admin/users/edit/<int:user_id>/', views.admin_edit_user_view, name='admin_edit_user'),
    path('admin/users/delete/<int:user_id>/', views.admin_delete_user_view, name='admin_delete_user'),

    # Product Management
    path('admin/products/', views.admin_products_view, name='admin_products'),
    path('admin/products/add/', views.admin_add_product_view, name='admin_add_product'),
    path('admin/products/edit/<int:product_id>/', views.admin_edit_product_view, name='admin_edit_product'),
    path('admin/products/delete/<int:product_id>/', views.admin_delete_product_view, name='admin_delete_product'),
]