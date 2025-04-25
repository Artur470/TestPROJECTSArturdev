from django.urls import path
from .views import register, login_view, profile
from . import views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('accounts/login/', login_view, name='login'),
    path('profile/', views.profile, name='profile'),

]
