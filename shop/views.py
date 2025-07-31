from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Product, CartItem, Favorite

# Create your views here.

def product_list(request):
    # Получаем параметры фильтрации
    category = request.GET.get('category', '')
    search = request.GET.get('search', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    
    # Базовый queryset
    products = Product.objects.all()
    
    # Применяем фильтры
    if category:
        products = products.filter(category__icontains=category)
    
    if search:
        products = products.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search) |
            Q(category__icontains=search)
        )
    
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass
    
    # Сортируем по дате создания
    products = products.order_by('-created_at')
    
    # Получаем уникальные категории для фильтра
    categories = Product.objects.values_list('category', flat=True).distinct().exclude(category='')
    
    # Получаем корзину пользователя
    cart_items = []
    cart_total = 0
    if request.session.session_key:
        cart_items = CartItem.objects.filter(session_key=request.session.session_key)
        cart_total = sum(item.get_total_price() for item in cart_items)
    
    # Получаем избранные товары
    favorites = []
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)
    elif request.session.session_key:
        favorites = Favorite.objects.filter(session_key=request.session.session_key).values_list('product_id', flat=True)
    
    context = {
        'products': products,
        'categories': categories,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_count': len(cart_items),
        'favorites': favorites,
        'favorites_count': len(favorites),
        'filters': {
            'category': category,
            'search': search,
            'min_price': min_price,
            'max_price': max_price,
        }
    }
    
    return render(request, 'shop/product_list.html', context)

def new_products(request):
    """Представление для новинок"""
    products = Product.objects.filter(is_new=True).order_by('-created_at')
    
    # Получаем корзину пользователя
    cart_items = []
    cart_total = 0
    if request.session.session_key:
        cart_items = CartItem.objects.filter(session_key=request.session.session_key)
        cart_total = sum(item.get_total_price() for item in cart_items)
    
    # Получаем избранные товары
    favorites = []
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)
    elif request.session.session_key:
        favorites = Favorite.objects.filter(session_key=request.session.session_key).values_list('product_id', flat=True)
    
    context = {
        'products': products,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_count': len(cart_items),
        'favorites': favorites,
        'favorites_count': len(favorites),
        'section_title': 'Новинки',
        'section_description': 'Самые свежие поступления в нашем магазине'
    }
    
    return render(request, 'shop/product_list.html', context)

def sale_products(request):
    """Представление для распродажи"""
    products = Product.objects.filter(is_sale=True).order_by('-created_at')
    
    # Получаем корзину пользователя
    cart_items = []
    cart_total = 0
    if request.session.session_key:
        cart_items = CartItem.objects.filter(session_key=request.session.session_key)
        cart_total = sum(item.get_total_price() for item in cart_items)
    
    # Получаем избранные товары
    favorites = []
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)
    elif request.session.session_key:
        favorites = Favorite.objects.filter(session_key=request.session.session_key).values_list('product_id', flat=True)
    
    context = {
        'products': products,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_count': len(cart_items),
        'favorites': favorites,
        'favorites_count': len(favorites),
        'section_title': 'Распродажа',
        'section_description': 'Специальные предложения и скидки'
    }
    
    return render(request, 'shop/product_list.html', context)

def popular_products(request):
    """Представление для популярных товаров"""
    products = Product.objects.filter(is_popular=True).order_by('-created_at')
    
    # Получаем корзину пользователя
    cart_items = []
    cart_total = 0
    if request.session.session_key:
        cart_items = CartItem.objects.filter(session_key=request.session.session_key)
        cart_total = sum(item.get_total_price() for item in cart_items)
    
    # Получаем избранные товары
    favorites = []
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)
    elif request.session.session_key:
        favorites = Favorite.objects.filter(session_key=request.session.session_key).values_list('product_id', flat=True)
    
    context = {
        'products': products,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_count': len(cart_items),
        'favorites': favorites,
        'favorites_count': len(favorites),
        'section_title': 'Популярное',
        'section_description': 'Самые востребованные товары'
    }
    
    return render(request, 'shop/product_list.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Получаем корзину пользователя
    cart_items = []
    cart_total = 0
    if request.session.session_key:
        cart_items = CartItem.objects.filter(session_key=request.session.session_key)
        cart_total = sum(item.get_total_price() for item in cart_items)
    
    # Проверяем, есть ли товар в избранном
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, product=product).exists()
    elif request.session.session_key:
        is_favorite = Favorite.objects.filter(session_key=request.session.session_key, product=product).exists()
    
    # Получаем похожие товары (той же категории)
    similar_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_count': len(cart_items),
        'is_favorite': is_favorite,
        'similar_products': similar_products,
    }
    
    return render(request, 'shop/product_detail.html', context)

def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        
        # Убеждаемся, что у пользователя есть сессия
        if not request.session.session_key:
            request.session.create()
        
        # Проверяем, есть ли уже этот товар в корзине
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            session_key=request.session.session_key,
            defaults={'quantity': 1}
        )
        
        if not created:
            # Если товар уже есть, увеличиваем количество
            cart_item.quantity += 1
            cart_item.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # AJAX запрос
            cart_items = CartItem.objects.filter(session_key=request.session.session_key)
            cart_total = sum(item.get_total_price() for item in cart_items)
            return JsonResponse({
                'success': True,
                'cart_count': len(cart_items),
                'cart_total': float(cart_total),
                'message': f'{product.name} добавлен в корзину'
            })
        
        return redirect('product_list')
    
    return redirect('product_list')

def remove_from_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, session_key=request.session.session_key)
        cart_item.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            cart_items = CartItem.objects.filter(session_key=request.session.session_key)
            cart_total = sum(item.get_total_price() for item in cart_items)
            return JsonResponse({
                'success': True,
                'cart_count': len(cart_items),
                'cart_total': float(cart_total)
            })
        
        return redirect('product_list')
    
    return redirect('product_list')

def update_cart_quantity(request, item_id):
    if request.method == 'POST':
        quantity = request.POST.get('quantity', 1)
        try:
            quantity = int(quantity)
            if quantity <= 0:
                cart_item = get_object_or_404(CartItem, id=item_id, session_key=request.session.session_key)
                cart_item.delete()
            else:
                cart_item = get_object_or_404(CartItem, id=item_id, session_key=request.session.session_key)
                cart_item.quantity = quantity
                cart_item.save()
        except ValueError:
            pass
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            cart_items = CartItem.objects.filter(session_key=request.session.session_key)
            cart_total = sum(item.get_total_price() for item in cart_items)
            return JsonResponse({
                'success': True,
                'cart_count': len(cart_items),
                'cart_total': float(cart_total)
            })
        
        return redirect('product_list')
    
    return redirect('product_list')

def cart_view(request):
    if not request.session.session_key:
        cart_items = []
        cart_total = 0
    else:
        cart_items = CartItem.objects.filter(session_key=request.session.session_key)
        cart_total = sum(item.get_total_price() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_count': len(cart_items)
    }
    
    return render(request, 'shop/cart.html', context)

def toggle_favorite(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        
        # Убеждаемся, что у пользователя есть сессия
        if not request.session.session_key:
            request.session.create()
        
        # Проверяем, есть ли уже этот товар в избранном
        if request.user.is_authenticated:
            favorite, created = Favorite.objects.get_or_create(
                user=request.user,
                product=product
            )
            if not created:
                favorite.delete()
                is_favorite = False
            else:
                is_favorite = True
        else:
            favorite, created = Favorite.objects.get_or_create(
                session_key=request.session.session_key,
                product=product
            )
            if not created:
                favorite.delete()
                is_favorite = False
            else:
                is_favorite = True
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Получаем обновленное количество избранных
            if request.user.is_authenticated:
                favorites_count = Favorite.objects.filter(user=request.user).count()
            else:
                favorites_count = Favorite.objects.filter(session_key=request.session.session_key).count()
            
            return JsonResponse({
                'success': True,
                'is_favorite': is_favorite,
                'favorites_count': favorites_count
            })
        
        return redirect('product_list')
    
    return redirect('product_list')

def favorites_view(request):
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user)
    elif request.session.session_key:
        favorites = Favorite.objects.filter(session_key=request.session.session_key)
    else:
        favorites = []
    
    products = [favorite.product for favorite in favorites]
    
    context = {
        'products': products,
        'favorites_count': len(products)
    }
    
    return render(request, 'shop/favorites.html', context)

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    
    return render(request, 'shop/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product_list')
        else:
            error_message = 'Неверное имя пользователя или пароль'
    else:
        error_message = None
    
    return render(request, 'shop/login.html', {'error_message': error_message})
