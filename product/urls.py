from django.urls import path
from .views import create_product, product_list
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
urlpatterns = [
    path('', product_list, name='product_list'),
    path('create/', views.create_product, name='create_product'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('<int:pk>/update/', views.product_update, name='product_update'),
    path('<int:product_id>/delete/', views.product_delete, name='product_delete'),
    path('create/brand/', views.create_brand, name='create_brand'),
    path('create-category/', views.create_category, name='create_category'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
