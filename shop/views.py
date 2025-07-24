from django.shortcuts import render
from .models import Product

# Create your views here.

def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'shop/product_list.html', {'products': products})
