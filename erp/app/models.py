from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .model_backup import Category, Product, Order, OrderItem, Cart, CartItem
from .forms import UserRegistrationForm, ProductForm, UserForm, CategoryForm
import json

# Helper function to check if user is admin
def is_admin(user):
    return user.is_staff

# Home view
def home(request):
    categories = Category.objects.all()[:6]
    # Use stock > 0 instead of in_stock=True
    featured_products = Product.objects.filter(stock__gt=0)[:8]
    
    context = {
        'categories': categories,
        'featured_products': featured_products,
    }
    return render(request, 'home.html', context)

# Product views
def product_list(request):
    # Use stock > 0 instead of in_stock=True
    products = Product.objects.filter(stock__gt=0)
    categories = Category.objects.all()
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
    
    # Category filter
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
    }
    return render(request, 'product_list.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Use stock > 0 instead of in_stock=True
    related_products = Product.objects.filter(
        category=product.category, 
        stock__gt=0
    ).exclude(id=product_id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'product_detail.html', context)

# Authentication views
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Muvaffaqiyatli kirdingiz!')
            return redirect('home')
        else:
            messages.error(request, 'Username yoki parol noto\'g\'ri!')
    return render(request, 'registration/login.html')

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} uchun hisob yaratildi!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'Muvaffaqiyatli chiqdingiz!')
    return redirect('home')

# Cart views
@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'cart.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if product is in stock
    if product.stock <= 0:
        messages.error(request, f'{product.name} hozirda omborda mavjud emas!')
        return redirect('product_detail', product_id=product_id)
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, 
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        # Check if adding one more item would exceed stock
        if cart_item.quantity + 1 > product.stock:
            messages.error(request, f'{product.name} uchun yetarli miqdor yo\'q!')
            return redirect('product_detail', product_id=product_id)
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'{product.name} savatchaga qo\'shildi!')
    return redirect('product_detail', product_id=product_id)

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'{product_name} savatchadan o\'chirildi!')
    return redirect('cart_view')

@login_required
def update_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            # Check if requested quantity is available in stock
            if quantity > cart_item.product.stock:
                messages.error(request, f'{cart_item.product.name} uchun faqat {cart_item.product.stock} dona mavjud!')
                return redirect('cart_view')
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        
        return redirect('cart_view')

# Order views
@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    if not cart_items:
        messages.error(request, 'Savatchangiz bo\'sh!')
        return redirect('cart_view')
    
    # Check stock availability for all items
    for item in cart_items:
        if item.quantity > item.product.stock:
            messages.error(request, f'{item.product.name} uchun yetarli miqdor yo\'q! Mavjud: {item.product.stock}')
            return redirect('cart_view')
    
    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address')
        
        # Create order
        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            shipping_address=shipping_address
        )
        
        # Create order items and update stock
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            # Reduce stock
            cart_item.product.stock -= cart_item.quantity
            cart_item.product.save()
        
        # Clear cart
        cart_items.delete()
        
        messages.success(request, 'Buyurtmangiz muvaffaqiyatli berildi!')
        return redirect('order_detail', order_id=order.id)
    
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'checkout.html', context)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {'order': order}
    return render(request, 'order_detail.html', context)

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)
    
    context = {'orders': orders}
    return render(request, 'my_orders.html', context)

# Admin views
@user_passes_test(is_admin)
def admin_dashboard(request):
    users_count = User.objects.count()
    products_count = Product.objects.count()
    orders_count = Order.objects.count()
    categories_count = Category.objects.count()
    
    recent_orders = Order.objects.order_by('-created_at')[:5]
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_products = Product.objects.order_by('-id')[:5]
    
    context = {
        'users_count': users_count,
        'products_count': products_count,
        'orders_count': orders_count,
        'categories_count': categories_count,
        'recent_orders': recent_orders,
        'recent_users': recent_users,
        'recent_products': recent_products,
    }
    return render(request, 'admin/dashboard.html', context)

# Admin Users Management
@user_passes_test(is_admin)
def admin_users(request):
    users = User.objects.all()
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        users = users.filter(
            Q(username__icontains=query) | 
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
    
    # Filter by staff status
    is_staff = request.GET.get('is_staff')
    if is_staff == 'true':
        users = users.filter(is_staff=True)
    elif is_staff == 'false':
        users = users.filter(is_staff=False)
    
    # Filter by active status
    is_active = request.GET.get('is_active')
    if is_active == 'true':
        users = users.filter(is_active=True)
    elif is_active == 'false':
        users = users.filter(is_active=False)
    
    users = users.order_by('-date_joined')
    
    # Pagination
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    
    context = {'users': users}
    return render(request, 'admin/users/list.html', context)

@user_passes_test(is_admin)
def admin_user_add(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password1')
            if password:
                user.set_password(password)
            user.save()
            messages.success(request, 'Foydalanuvchi muvaffaqiyatli qo\'shildi!')
            return redirect('admin_users')
    else:
        form = UserForm()
    
    context = {'form': form}
    return render(request, 'admin/users/add.html', context)

@user_passes_test(is_admin)
def admin_user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password1')
            if password:
                user.set_password(password)
            user.save()
            messages.success(request, 'Foydalanuvchi ma\'lumotlari yangilandi!')
            return redirect('admin_users')
    else:
        form = UserForm(instance=user)
    
    context = {'form': form, 'user': user}
    return render(request, 'admin/users/edit.html', context)

@user_passes_test(is_admin)
def admin_user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'{username} foydalanuvchisi o\'chirildi!')
        return redirect('admin_users')
    
    context = {'user': user}
    return render(request, 'admin/users/delete.html', context)

# Admin Products Management
@user_passes_test(is_admin)
def admin_products(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Filter by stock status (replace in_stock with stock)
    stock_status = request.GET.get('stock_status')
    if stock_status == 'in_stock':
        products = products.filter(stock__gt=0)
    elif stock_status == 'out_of_stock':
        products = products.filter(stock=0)
    
    products = products.order_by('-id')
    
    # Pagination
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'admin/products/list.html', context)

@user_passes_test(is_admin)
def admin_product_add(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mahsulot muvaffaqiyatli qo\'shildi!')
            return redirect('admin_products')
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'categories': categories,
    }
    return render(request, 'admin/products/add.html', context)

@user_passes_test(is_admin)
def admin_product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mahsulot ma\'lumotlari yangilandi!')
            return redirect('admin_products')
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product,
        'categories': categories,
    }
    return render(request, 'admin/products/edit.html', context)

@user_passes_test(is_admin)
def admin_product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'{product_name} mahsuloti o\'chirildi!')
        return redirect('admin_products')
    
    context = {'product': product}
    return render(request, 'admin/products/delete.html', context)

# Admin Categories Management
@user_passes_test(is_admin)
def admin_categories(request):
    categories = Category.objects.all().order_by('name')
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        categories = categories.filter(name__icontains=query)
    
    # Pagination
    paginator = Paginator(categories, 20)
    page_number = request.GET.get('page')
    categories = paginator.get_page(page_number)
    
    context = {'categories': categories}
    return render(request, 'admin/categories/list.html', context)

@user_passes_test(is_admin)
def admin_category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kategoriya muvaffaqiyatli qo\'shildi!')
            return redirect('admin_categories')
    else:
        form = CategoryForm()
    
    context = {'form': form}
    return render(request, 'admin/categories/add.html', context)

@user_passes_test(is_admin)
def admin_category_edit(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kategoriya ma\'lumotlari yangilandi!')
            return redirect('admin_categories')
    else:
        form = CategoryForm(instance=category)
    
    context = {'form': form, 'category': category}
    return render(request, 'admin/categories/edit.html', context)

@user_passes_test(is_admin)
def admin_category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'{category_name} kategoriyasi o\'chirildi!')
        return redirect('admin_categories')
    
    context = {'category': category}
    return render(request, 'admin/categories/delete.html', context)

# Admin Orders Management
@user_passes_test(is_admin)
def admin_orders(request):
    orders = Order.objects.all()
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        orders = orders.filter(
            Q(user__username__icontains=query) |
            Q(user__email__icontains=query) |
            Q(id__icontains=query)
        )
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)
    
    orders = orders.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)
    
    context = {'orders': orders}
    return render(request, 'admin/orders/list.html', context)

@user_passes_test(is_admin)
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, 'Buyurtma holati yangilandi!')
            return redirect('admin_order_detail', order_id=order_id)
    
    context = {'order': order}
    return render(request, 'admin/orders/detail.html', context)