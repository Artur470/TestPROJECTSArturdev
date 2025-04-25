from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import IsAdminUser
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import views as auth_views


schema_view = get_schema_view(
    openapi.Info(
        title="Продуктовый API",
        default_version='v1',
        description="Документация API (CRUD, связи, сокеты и т.д.)",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=False,
    permission_classes=(IsAdminUser,),
    authentication_classes=[JWTAuthentication, BasicAuthentication, SessionAuthentication],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include("core.urls")),
    path('', include("product.urls")),


    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]
