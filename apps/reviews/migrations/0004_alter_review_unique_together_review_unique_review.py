# Generated by Django 5.1 on 2024-09-17 08:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0004_alter_listing_owner_viewhistory'),
        ('reviews', '0003_rename_reviewer_review_user_alter_review_rating_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('listing', 'user'), name='unique_review'),
        ),
    ]
