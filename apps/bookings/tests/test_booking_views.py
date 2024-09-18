from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.bookings.models import Booking
from apps.listings.models import Listing
from apps.users.models import User

class BookingViewSetTest(TestCase):
    def setUp(self):
        # Настраиваем тестовый клиент и создаем тестовых пользователей и объявление
        self.client = APIClient()
        self.landlord = User.objects.create_user(
            email='landlord@example.com',
            password='password',
            first_name='John',
            last_name='Doe',
            position='LANDLORD'
        )
        self.tenant = User.objects.create_user(
            email='tenant@example.com',
            password='password',
            first_name='Jane',
            last_name='Doe',
            position='TENANT'
        )
        self.listing = Listing.objects.create(
            title='Test Listing',
            description='Test Description',
            location='Berlin',
            price=1000,
            rooms=3,
            housing_type='APARTMENT',
            owner=self.landlord
        )

        self.client.force_authenticate(user=self.tenant)

    def test_booking_creation(self):
        # Данные для бронирования
        data = {
            'listing': self.listing.id,
            'start_date': '2024-11-01',
            'end_date': '2024-11-10'
        }

        # Выполняем запрос на создание бронирования
        response = self.client.post(reverse('booking-list'), data, format='json')

        # Проверяем успешность создания бронирования
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем данные ответа
        self.assertEqual(response.data['listing'], self.listing.id)
        self.assertEqual(response.data['start_date'], '2024-11-01')
        self.assertEqual(response.data['end_date'], '2024-11-10')

    def test_booking_creation_conflict(self):
        """Тестирует, что нельзя создать бронирование на пересекающиеся даты."""
        # Создаем первое бронирование
        Booking.objects.create(
            listing=self.listing,
            tenant=self.tenant,
            start_date='2024-11-01',
            end_date='2024-11-10'
        )

        # Пытаемся создать пересекающееся бронирование
        conflict_data = {
            'listing': self.listing.id,
            'start_date': '2024-11-05',
            'end_date': '2024-11-15'
        }

        response = self.client.post(reverse('booking-list'), conflict_data, format='json')

        # Проверяем, что бронирование не создается из-за конфликта дат
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Для этого объявления уже есть бронирование на эти даты.', str(response.data))

    def test_booking_creation_forbidden_non_tenant(self):
        """Тестирует, что не-арендатор не может создавать бронирования."""
        # Аутентифицируем Landlord
        self.client.force_authenticate(user=self.landlord)

        data = {
            'listing': self.listing.id,
            'start_date': '2024-11-01',
            'end_date': '2024-11-10'
        }

        response = self.client.post(reverse('booking-list'), data, format='json')

        # Проверяем, что Landlord не может создать бронирование
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('Только арендаторы могут создавать бронирования.', str(response.data))