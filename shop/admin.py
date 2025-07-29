from django.contrib import admin
from .models import Product, CartItem, Favorite

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description', 'category')
    ordering = ('-created_at',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'session_key', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('product__name', 'session_key')
    ordering = ('-created_at',)

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'session_key', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('product__name', 'user__username', 'session_key')
    ordering = ('-created_at',)
