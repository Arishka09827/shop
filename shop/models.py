from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    name = models.CharField('Название', max_length=120)
    description = models.TextField('Описание', blank=True)
    price = models.DecimalField('Цена', max_digits=8, decimal_places=2)
    old_price = models.DecimalField('Старая цена', max_digits=8, decimal_places=2, null=True, blank=True)
    image = models.ImageField('Изображение', upload_to='products/')
    category = models.CharField('Категория', max_length=60, blank=True)
    is_new = models.BooleanField('Новинка', default=False)
    is_popular = models.BooleanField('Популярное', default=False)
    is_sale = models.BooleanField('Распродажа', default=False)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    def __str__(self):
        return self.name
    
    @property
    def discount_percent(self):
        """Вычисляет процент скидки"""
        if self.old_price and self.old_price > self.price:
            return int(((self.old_price - self.price) / self.old_price) * 100)
        return 0

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Количество', default=1)
    session_key = models.CharField('Ключ сессии', max_length=40)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def get_total_price(self):
        return self.product.price * self.quantity

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    session_key = models.CharField('Ключ сессии', max_length=40, null=True, blank=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        unique_together = [['user', 'product'], ['session_key', 'product']]

    def __str__(self):
        if self.user:
            return f"{self.user.username} - {self.product.name}"
        return f"Session {self.session_key} - {self.product.name}"
