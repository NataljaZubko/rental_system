from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from .models import Review
from .serializers import ReviewSerializer
from apps.users.permissions import IsTenant
from .permissions import IsAuthenticatedOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsTenant()]
        return [IsAuthenticatedOrReadOnly()]

    def get_queryset(self):
        # Фильтрация отзывов по конкретному объявлению
        listing_id = self.request.query_params.get('listing')
        if listing_id:
            return self.queryset.filter(listing__id=listing_id)
        return self.queryset

    def perform_create(self, serializer):
        # Проверка на существование отзыва для данного объявления и пользователя
        user = self.request.user
        listing = serializer.validated_data['listing']

        if Review.objects.filter(listing=listing, user=user).exists():
            raise ValidationError("Вы уже оставляли отзыв на это объявление.")

        # Сохраняем объект с текущим пользователем как автором отзыва
        serializer.save(user=user)