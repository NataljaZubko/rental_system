from rest_framework import serializers
from apps.listings.models import Listing
from apps.users.models import User

class ListingDetailSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='email', read_only=True)

    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'location', 'price', 'rooms', 'housing_type',
            'is_active', 'owner', 'views_count', 'created_at', 'updated_at'
        ]

class CreateUpdateListingSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='email', read_only=True)

    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'location', 'price', 'rooms', 'housing_type',
            'is_active', 'owner', 'views_count', 'created_at', 'updated_at'
        ]

    def create(self, validated_data):
        # Убираем передачу owner через validated_data
        return Listing.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.location = validated_data.get('location', instance.location)
        instance.price = validated_data.get('price', instance.price)
        instance.rooms = validated_data.get('rooms', instance.rooms)
        instance.housing_type = validated_data.get('housing_type', instance.housing_type)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance