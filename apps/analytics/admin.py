from django.contrib import admin
from .models import SearchHistory, ViewHistory

@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'search_term', 'created_at')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(ViewHistory)
class ViewHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'viewed_at')
    list_filter = ('viewed_at',)
    ordering = ('-viewed_at',)