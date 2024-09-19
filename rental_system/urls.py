"""
URL configuration for rental_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from apps.users.views import UserRegisterView, UserListView
from apps.listings.views import ListingViewSet
from apps.bookings.views import BookingViewSet
from apps.analytics.views import SearchView, PopularSearchView  # Исправляем импорт
from apps.reviews.views import ReviewViewSet

# Создаем основную страницу
def home(request):
    return HttpResponse("Welcome to the Rental System!")

# Настройка для Swagger и ReDoc документации
schema_view = get_schema_view(
    openapi.Info(
        title="Rental System API",
        default_version='v1',
        description="API documentation for the Rental System",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@rental-system.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# Настраиваем DefaultRouter
router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'reviews', ReviewViewSet, basename='review')

# Основные URL паттерны
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),  # Включаем роуты от DefaultRouter
    path('api/v1/users/', include('apps.users.urls')),
    path('api/v1/listings/', include('apps.listings.urls')),
    path('api/v1/bookings/', include('apps.bookings.urls')),
    path('api/v1/reviews/', include('apps.reviews.urls')),
    path('api/v1/analytics/', include('apps.analytics.urls')),  # Добавляем маршруты аналитики
    path('', home),  # Главная страница
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

