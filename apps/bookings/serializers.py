from rest_framework import serializers
from apps.bookings.models import Booking
from apps.listings.models import Listing


class CreateUpdateBookingSerializer(serializers.ModelSerializer):
    listing = serializers.SlugRelatedField(
        slug_field='id',  # Здесь передаем ID объявления
        queryset=Listing.objects.all()
    )

    class Meta:
        model = Booking
        fields = ['id', 'listing', 'start_date', 'end_date', 'status']
        read_only_fields = ['status', 'tenant']  # Поле tenant будет назначаться автоматически

    def validate(self, data):
        # Проверка на корректность дат
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("Дата начала бронирования не может быть позже даты окончания.")

        # Проверка на пересекающиеся бронирования
        listing = data['listing']
        start_date = data['start_date']
        end_date = data['end_date']

        existing_bookings = Booking.objects.filter(listing=listing).filter(
            start_date__lte=end_date, end_date__gte=start_date
        )

        if existing_bookings.exists():
            raise serializers.ValidationError("Для этого объявления уже есть бронирование на эти даты.")

        return data

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class BookingDetailSerializer(serializers.ModelSerializer):
    listing = serializers.SlugRelatedField(read_only=True, slug_field='title')
    tenant = serializers.SlugRelatedField(read_only=True, slug_field='email')

    class Meta:
        model = Booking
        fields = ['id', 'listing', 'tenant', 'start_date', 'end_date', 'status']
        read_only_fields = ['tenant', 'status']