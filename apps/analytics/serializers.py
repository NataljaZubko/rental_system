from rest_framework import serializers
from .models import SearchHistory, PopularSearch, ViewHistory
from apps.listings.serializers import ListingDetailSerializer

class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ['search_term', 'created_at']

class PopularSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopularSearch
        fields = ['search_term', 'search_count']

class ViewHistorySerializer(serializers.ModelSerializer):
    listing = ListingDetailSerializer(read_only=True)  # Используем подробный сериализатор для отображения информации об объявлении

    class Meta:
        model = ViewHistory
        fields = ['listing', 'viewed_at']