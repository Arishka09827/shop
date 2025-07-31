from django.contrib import admin
from .models import Product, CartItem, Favorite

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'old_price', 'is_new', 'is_popular', 'is_sale', 'created_at')
    list_filter = ('category', 'is_new', 'is_popular', 'is_sale', 'created_at')
    search_fields = ('name', 'description', 'category')
    ordering = ('-created_at',)
    list_editable = ('is_new', 'is_popular', 'is_sale')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'category', 'image')
        }),
        ('Цены', {
            'fields': ('price', 'old_price')
        }),
        ('Статусы', {
            'fields': ('is_new', 'is_popular', 'is_sale'),
            'classes': ('collapse',)
        }),
    )

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
