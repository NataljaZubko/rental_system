from django.contrib import admin


def register_models():
    from .models import Listing

    @admin.register(Listing)
    class ListingAdmin(admin.ModelAdmin):
        list_display = ('title', 'owner', 'price', 'created_at', 'updated_at')
        search_fields = ('title', 'description', 'owner__email')
        list_filter = ('price', 'created_at', 'updated_at')
        ordering = ('-created_at',)


register_models()
