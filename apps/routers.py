from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.listings.views import ListingViewSet
from apps.bookings.views import BookingViewSet
from apps.reviews.views import ReviewViewSet
from apps.analytics.views import SearchView, PopularSearchView

router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),  # Включаем маршруты роутера
    path('analytics/search/', SearchView.as_view(), name='search'),  # Поиск аналитики
    path('analytics/popular-searches/', PopularSearchView.as_view(), name='popular-searches'),  # Популярные запросы
]