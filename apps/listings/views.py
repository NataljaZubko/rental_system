from django.db import models  # Добавляем этот импорт для работы с аннотациями и подсчётами
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Listing, ViewHistory
from .serializers import ListingDetailSerializer, CreateUpdateListingSerializer
from apps.users.permissions import IsLandlord
from .permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]  # Подключаем фильтрацию и сортировку
    filterset_fields = ['price', 'rooms', 'location']  # Поля для фильтрации
    ordering_fields = ['id', 'price', 'rooms', 'is_active', 'owner',
                       'views_count', 'created_at', 'updated_at']  # Поля для сортировки

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ListingDetailSerializer
        return CreateUpdateListingSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsLandlord()]
        return [IsAuthenticatedOrReadOnly()]  # Используем импорт из listings.permissions

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.increment_views()  # Инкрементируем просмотры
        if request.user.is_authenticated:
            ViewHistory.objects.create(user=request.user, listing=instance)  # Сохраняем историю просмотров
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_update(self, serializer):
        listing = self.get_object()
        if listing.owner != self.request.user:
            return Response({'detail': 'Только владелец может обновлять это объявление.'}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            return Response({'detail': 'Только владелец может удалить это объявление.'}, status=status.HTTP_403_FORBIDDEN)
        instance.delete()

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.query_params.get('sort_by')

        if sort_by == 'views':
            return queryset.order_by('-views_count')
        elif sort_by == 'reviews':
            return queryset.annotate(num_reviews=models.Count('reviews')).order_by('-num_reviews')

        return queryset