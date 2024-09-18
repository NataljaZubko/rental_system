# from django.db import models
# from apps.users.models import User
# from apps.listings.models import Listing
#
# class Review(models.Model):
#     RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # Рейтинг от 1 до 5
#
#     listing = models.ForeignKey(Listing, related_name='reviews', on_delete=models.CASCADE)
#     user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
#     rating = models.IntegerField(choices=RATING_CHOICES)
#     comment = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         unique_together = ('listing', 'user')  # Один отзыв на одного пользователя
#
#     def __str__(self):
#         return f"Review by {self.user} for {self.listing}"

from django.db import models
from apps.users.models import User
from apps.listings.models import Listing

class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # Рейтинг от 1 до 5

    listing = models.ForeignKey(Listing, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['listing', 'user'], name='unique_review')
        ]  # Один отзыв на одного пользователя для каждого объявления

    def __str__(self):
        return f"Review by {self.user} for {self.listing}"