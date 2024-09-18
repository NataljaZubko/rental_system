from django.db import models
from django.conf import settings

class SearchHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='search_history', on_delete=models.CASCADE)
    search_term = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} searched for {self.search_term} on {self.created_at}"

class ViewHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='view_history', on_delete=models.CASCADE)
    listing = models.ForeignKey('listings.Listing', related_name='view_histories', on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} viewed {self.listing} on {self.viewed_at}"

class PopularSearch(models.Model):
    search_term = models.CharField(max_length=255, unique=True)
    search_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.search_term} (count: {self.search_count})"