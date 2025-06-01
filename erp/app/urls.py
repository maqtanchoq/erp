from django.urls import path
from . import views



urlpatterns = [
    # Public views
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    
    # Authentication
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    
    # Cart and Orders
    path('cart/', views.cart_view, name='cart_view'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('my-orders/', views.my_orders, name='my_orders'),
    
    # Admin Dashboard
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Admin Users Management
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/users/add/', views.admin_user_add, name='admin_user_add'),
    path('admin/users/<int:user_id>/edit/', views.admin_user_edit, name='admin_user_edit'),
    path('admin/users/<int:user_id>/delete/', views.admin_user_delete, name='admin_user_delete'),
    
    # Admin Products Management
    path('admin/products/', views.admin_products, name='admin_products'),
    path('admin/products/add/', views.admin_product_add, name='admin_product_add'),
    path('admin/products/<int:product_id>/edit/', views.admin_product_edit, name='admin_product_edit'),
    path('admin/products/<int:product_id>/delete/', views.admin_product_delete, name='admin_product_delete'),
    
    # Admin Categories Management
    path('admin/categories/', views.admin_categories, name='admin_categories'),
    path('admin/categories/add/', views.admin_category_add, name='admin_category_add'),
    path('admin/categories/<int:category_id>/edit/', views.admin_category_edit, name='admin_category_edit'),
    path('admin/categories/<int:category_id>/delete/', views.admin_category_delete, name='admin_category_delete'),
    
    # Admin Orders Management
    path('admin/orders/', views.admin_orders, name='admin_orders'),
    path('admin/orders/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
]