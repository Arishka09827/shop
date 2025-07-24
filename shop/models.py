from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField('Название', max_length=120)
    description = models.TextField('Описание', blank=True)
    price = models.DecimalField('Цена', max_digits=8, decimal_places=2)
    image = models.ImageField('Изображение', upload_to='products/')
    category = models.CharField('Категория', max_length=60, blank=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    def __str__(self):
        return self.name
