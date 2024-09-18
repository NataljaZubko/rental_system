from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookingViewSet

# Создаем роутер для автоматической генерации маршрутов
router = DefaultRouter()

# Регистрация маршрутов для бронирований
router.register(r'', BookingViewSet, basename='booking')

# Определение urlpatterns с использованием сгенерированных маршрутов
urlpatterns = [
    path('', include(router.urls)),  # Подключаем маршруты роутера
]