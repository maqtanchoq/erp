from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone # For default created_at values

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now) # Used in CategoryAdmin

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories" # Optional: for better display in admin

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    in_stock = models.BooleanField(default=True)  # <--- ADD THIS LINE
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products') # SET_NULL is often better than CASCADE for category
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0) # Used in ProductAdmin
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    featured = models.BooleanField(default=False) # Used in ProductAdmin
    created_at = models.DateTimeField(default=timezone.now) # Used in ProductAdmin
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now) # Used in CartAdmin

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField() # Assuming this is still needed from your views
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending') # Used in OrderAdmin
    created_at = models.DateTimeField(default=timezone.now) # Used in OrderAdmin
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    class Meta:
        ordering = ['-created_at'] # Consistent with admin ordering

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE) # Consider on_delete=models.SET_NULL if you want to keep order items even if product is deleted
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2) # Price at the time of order

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for Order {self.order.id}"