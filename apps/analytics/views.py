from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import SearchHistory, PopularSearch, ViewHistory
from .serializers import SearchHistorySerializer, PopularSearchSerializer, ViewHistorySerializer
from .permissions import IsAuthenticatedOrReadOnly
from apps.listings.models import Listing  # Модель объявлений


class SearchView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]  # Доступ только на чтение для всех пользователей

    def get(self, request):
        search_term = request.query_params.get('search_term', '')

        if search_term:
            # Если пользователь авторизован, сохраняем историю поиска
            if request.user.is_authenticated:
                SearchHistory.objects.create(user=request.user, search_term=search_term)

        # Возвращаем объявления, которые соответствуют поисковому запросу
        listings = Listing.objects.filter(title__icontains=search_term)
        return Response({"results": [listing.title for listing in listings]})


class PopularSearchView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        popular_searches = PopularSearch.objects.order_by('-search_count')[:10]
        serializer = PopularSearchSerializer(popular_searches, many=True)
        return Response(serializer.data)


class ListingDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        try:
            listing = Listing.objects.get(pk=pk)
            # Если пользователь авторизован, сохраняем историю просмотра
            if request.user.is_authenticated:
                ViewHistory.objects.create(user=request.user, listing=listing)
            return Response({
                "title": listing.title,
                "description": listing.description,
                "price": listing.price,
                "location": listing.location,
            })
        except Listing.DoesNotExist:
            return Response({"detail": "Объявление не найдено"}, status=status.HTTP_404_NOT_FOUND)


class ViewHistoryView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        # Если пользователь не аутентифицирован, возвращаем пустой ответ или другое сообщение
        if not request.user.is_authenticated:
            return Response({"detail": "Для просмотра истории необходимо авторизоваться."}, status=status.HTTP_200_OK)

        # Если пользователь авторизован, возвращаем историю просмотров
        view_history = ViewHistory.objects.filter(user=request.user).order_by('-viewed_at')
        serializer = ViewHistorySerializer(view_history, many=True)
        return Response(serializer.data)


class SearchHistoryView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        # Если пользователь не аутентифицирован, возвращаем пустой ответ или другое сообщение
        if not request.user.is_authenticated:
            return Response({"detail": "Для просмотра истории поиска необходимо авторизоваться."}, status=status.HTTP_200_OK)

        # Получаем историю поиска авторизованного пользователя
        search_history = SearchHistory.objects.filter(user=request.user).order_by('-created_at')
        serializer = SearchHistorySerializer(search_history, many=True)
        return Response(serializer.data)