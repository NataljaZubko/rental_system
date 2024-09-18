from django.db import models
from django.conf import settings
from apps.users.models import User

class Listing(models.Model):
    HOUSING_TYPE_CHOICES = [
        ('APARTMENT', 'Квартира'),
        ('HOUSE', 'Дом'),
        ('STUDIO', 'Студия'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rooms = models.PositiveIntegerField()
    housing_type = models.CharField(max_length=20, choices=HOUSING_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)  # Используем строковую ссылку на модель
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title



    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])


class ViewHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='listing_view_history', on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, related_name='view_history', on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} viewed {self.listing} on {self.viewed_at}"

