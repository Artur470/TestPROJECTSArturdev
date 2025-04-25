from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import ProductForm, ProductFormUpdate, BrandForm, CategoryForm
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from drf_yasg import openapi

from .models import Product, Brand, Category
from drf_yasg.utils import swagger_auto_schema
from core.models import GlobalNotification
from rest_framework.decorators import api_view

@swagger_auto_schema(
    method='get',
    operation_description="Получение списка продуктов с возможностью фильтрации по бренду и категории.",
    manual_parameters=[
        # Определяем параметры для фильтрации
        openapi.Parameter('brand', openapi.IN_QUERY, description="ID бренда для фильтрации", type=openapi.TYPE_INTEGER),
        openapi.Parameter('category', openapi.IN_QUERY, description="ID категории для фильтрации", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: openapi.Response(
            description="Список продуктов, брендов, категорий и уведомлений",
            examples={
                "application/json": {
                    "products": [
                        {
                            "id": 1,
                            "name": "Product Name",  # Название продукта
                            "description": "Product Description",  # Описание продукта
                            "price": 100.00,  # Цена продукта
                            "brand": {
                                "id": 1,
                                "name": "Brand Name"  # Информация о бренде
                            },
                            "categories": [
                                {
                                    "id": 1,
                                    "name": "Category Name"  # Информация о категории
                                }
                            ]
                        }
                    ],
                    "brands": [
                        {
                            "id": 1,
                            "name": "Brand Name"  # Список брендов
                        }
                    ],
                    "categories": [
                        {
                            "id": 1,
                            "name": "Category Name"  # Список категорий
                        }
                    ],
                    "notifications": [
                        {
                            "id": 1,
                            "message": "Global notification message",  # Сообщение уведомления
                            "created_at": "2025-04-25T10:00:00Z"  # Время создания уведомления
                        }
                    ]
                }
            }
        )
    }
)
@api_view(['GET'])

def product_list(request):
    """
    Возвращает список продуктов с возможностью фильтрации по бренду и категории.
    Также передаются последние 5 глобальных уведомлений.
    """
    # Получаем глобальные уведомления
    notifications = GlobalNotification.objects.order_by('-created_at')[:5]  # последние 5

    # Получаем все бренды и категории для фильтрации
    brands = Brand.objects.all()
    categories = Category.objects.all()

    # Получаем id выбранного бренда и категории из GET-запроса
    selected_brand_id = request.GET.get('brand', None)
    selected_category_id = request.GET.get('category', None)

    # Фильтрация по бренду
    products = Product.objects.all()

    if selected_brand_id:
        products = products.filter(brand_id=selected_brand_id)

    # Фильтрация по категории
    if selected_category_id:
        products = products.filter(categories__id=selected_category_id)

    # Проверяем, является ли пользователь суперпользователем
    is_superuser = request.user.is_superuser

    return render(request, 'product_list.html', {
        'products': products,
        'brands': brands,
        'categories': categories,
        'selected_brand_id': selected_brand_id,
        'selected_category_id': selected_category_id,
        'notifications': notifications,  # передаем уведомления в шаблон
        'is_superuser': is_superuser,  # передаем информацию о суперпользователе
    })

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # Передаем request.FILES для обработки файлов
        if form.is_valid():
            form.save()
            # Перенаправляем на страницу с продуктами
            return redirect('product_list')  # Перенаправляем на список продуктов
    else:
        form = ProductForm()

    return render(request, 'create_product.html', {'form': form})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductFormUpdate(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id=product.pk)
    else:
        form = ProductFormUpdate(instance=product)
    return render(request, 'product_update.html', {'form': form})


@swagger_auto_schema(
    methods=['post'],
    operation_description="Удаление продукта. GET-запрос для отображения страницы подтверждения удаления, POST-запрос для удаления продукта.",
    responses={
        200: openapi.Response(description="Продукт успешно удален."),
        404: openapi.Response(description="Продукт не найден."),
        405: openapi.Response(description="Метод не разрешен.")
    }
)
@api_view([ 'POST'])
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.delete()
        return redirect('product_list')  # Название URL для списка продуктов

    return render(request, 'product/confirm_delete.html', {'product': product})\







@swagger_auto_schema(
    methods=['get', 'post'],
    operation_description="Создание нового бренда. GET-запрос для отображения формы, POST-запрос для создания бренда.",
    responses={
        200: openapi.Response(description="Форма для создания бренда или успешное создание."),
        405: openapi.Response(description="Метод не разрешен.")
    }
)
@api_view(['GET', 'POST'])
def create_brand(request):
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Перенаправление на страницу с продуктами
    else:
        form = BrandForm()

    return render(request, 'create_brand.html', {'form': form})

@swagger_auto_schema(
    methods=['get', 'post'],
    operation_description="Создание новой категории. GET-запрос для отображения формы, POST-запрос для создания категории.",
    responses={
        200: openapi.Response(description="Форма для создания категории или успешное создание."),
        405: openapi.Response(description="Метод не разрешен.")
    }
)
@api_view(['GET', 'POST'])
def create_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Перенаправление на список продуктов
    else:
        form = CategoryForm()

    return render(request, 'create_category.html', {'form': form})