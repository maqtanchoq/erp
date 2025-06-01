from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Category, Product, Order, OrderItem, Cart, CartItem

# Unregister the default User admin
admin.site.unregister(User)

# Custom User Admin
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'featured', 'created_at')
    list_filter = ('category', 'featured', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock', 'featured')
    ordering = ('-created_at',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__email')
    list_editable = ('status',)
    inlines = [OrderItemInline]
    ordering = ('-created_at',)

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)
    inlines = [CartItemInline]

# Customize admin site
admin.site.site_header = "Sanjarbek Admin Panel"
admin.site.site_title = "Sanjarbek Admin"
admin.site.index_title = "Sanjarbek boshqaruv paneli"
