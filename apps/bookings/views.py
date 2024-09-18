from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .models import Booking
from .serializers import CreateUpdateBookingSerializer, BookingDetailSerializer
from .permissions import IsAuthenticatedOrReadOnly
from django.core.mail import send_mail
from rest_framework.filters import OrderingFilter

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['listing', 'start_date', 'end_date']  # Поля для фильтрации
    ordering_fields = ['id', 'listing', 'start_date', 'end_date']  # Поля для сортировки

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return BookingDetailSerializer
        return CreateUpdateBookingSerializer

    def get_permissions(self):
        # Если действие на запись (создание, обновление, удаление), требуется авторизация
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        # Для просмотра бронирований используем IsAuthenticatedOrReadOnly
        return [IsAuthenticatedOrReadOnly()]

    def perform_create(self, serializer):
        tenant = self.request.user

        # Проверяем, что пользователь является арендатором
        if tenant.position != 'TENANT':
            raise PermissionDenied(detail="Только арендаторы могут создавать бронирования.")

        # Получаем данные из сериализатора
        listing = serializer.validated_data['listing']
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']

        # Проверяем пересечение дат бронирования
        overlapping_bookings = Booking.objects.filter(listing=listing).filter(
            start_date__lte=end_date, end_date__gte=start_date
        )

        if overlapping_bookings.exists():
            raise ValidationError("Для этого объявления уже есть бронирование на эти даты.")

        # Сохраняем бронирование с текущим пользователем как tenant
        booking = serializer.save(tenant=tenant)

        # Отправка письма владельцу объявления
        owner_email = listing.owner.email  # Получаем email владельца объявления
        subject = 'Новое бронирование на ваше объявление'
        message = (
            f"Уважаемый {listing.owner.first_name},\n\n"
            f"Ваше объявление '{listing.title}' было забронировано пользователем {tenant.email} "
            f"с {start_date} по {end_date}.\n\n"
            "Пожалуйста, свяжитесь с арендатором для дальнейших действий."
        )

        # Отправляем email
        send_mail(
            subject,
            message,
            'noreply@example.com',  # Адрес отправителя
            [owner_email],  # Адрес получателя (владелец объявления)
            fail_silently=False,
        )

    def perform_update(self, serializer):
        tenant = self.request.user
        # Проверяем, что пользователь является арендатором
        if tenant.position != 'TENANT':
            raise PermissionDenied(detail="Только арендаторы могут обновлять бронирования.")

        # Обновление происходит без пересечений, так как даты не меняются.
        serializer.save(tenant=tenant)

    def destroy(self, request, *args, **kwargs):
        booking = self.get_object()
        # Допустим, только арендатор или администратор может удалить бронирование
        if request.user != booking.tenant and not request.user.is_staff:
            raise PermissionDenied(detail="Вы не можете удалить это бронирование.")
        return super().destroy(request, *args, **kwargs)