from django import forms
from .models import Product, Brand, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image','brand','categories']  # добавьте все нужные поля


class ProductFormUpdate(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
