from django.urls import path
from .views import SearchView, PopularSearchView, ListingDetailView, ViewHistoryView, SearchHistoryView

urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),
    path('popular-searches/', PopularSearchView.as_view(), name='popular-searches'),
    path('listings/<int:pk>/', ListingDetailView.as_view(), name='listing-detail'),
    path('view-history/', ViewHistoryView.as_view(), name='view-history'),
    path('search-history/', SearchHistoryView.as_view(), name='search-history'),
]