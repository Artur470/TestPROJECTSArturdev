from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Create your models here.
class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)  # Связь с Brand
    categories = models.ManyToManyField(Category, related_name='products', blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')  # если изображение необходимо

    def __str__(self):
        return self.name

