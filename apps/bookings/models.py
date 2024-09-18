from django.db import models
from apps.listings.models import Listing
from apps.users.models import User


class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'В ожидании'),
        ('CONFIRMED', 'Подтверждено'),
        ('CANCELLED', 'Отменено'),
    ]

    listing = models.ForeignKey(Listing, related_name='bookings', on_delete=models.CASCADE)
    tenant = models.ForeignKey(User, related_name='bookings', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.listing.title} - {self.tenant.email}"


    class Meta:
        ordering = ['-created_at']  # По умолчанию сортировать по дате создания (новые бронирования первыми)
