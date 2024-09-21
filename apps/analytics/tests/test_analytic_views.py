from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.users.models import User
from apps.listings.models import Listing
from apps.analytics.models import ViewHistory, SearchHistory


class AnalyticsViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Создаем тестового пользователя и авторизуем его
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )
        self.client.force_authenticate(user=self.user)

        # Создаем тестовое объявление
        self.listing = Listing.objects.create(
            title='Test Listing',
            description='Test description',
            price=1000,
            rooms=2,
            housing_type='APARTMENT',
            owner=self.user
        )

        # Создаем запись в истории просмотров
        ViewHistory.objects.create(user=self.user, listing=self.listing)

        # Создаем запись в истории поиска
        SearchHistory.objects.create(user=self.user, search_term='Test search')

    def test_view_history(self):
        # Тестируем просмотр истории просмотров
        response = self.client.get('/api/v1/analytics/view-history/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что данные истории просмотров корректны
        self.assertEqual(len(response.data), 1)
        # Сравниваем id объявления
        self.assertEqual(response.data[0]['listing']['id'], self.listing.id)

    def test_search_history(self):
        # Тестируем просмотр истории поиска
        response = self.client.get('/api/v1/analytics/search-history/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что данные истории поиска корректны
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['search_term'], 'Test search')

    def test_unauthenticated_view_history(self):
        # Тестируем историю просмотров для неавторизованного пользователя
        self.client.logout()  # Удаляем аутентификацию
        response = self.client.get('/api/v1/analytics/view-history/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Изменено на 401
        self.assertEqual(response.data['detail'], 'Для просмотра истории необходимо авторизоваться.')

    def test_unauthenticated_search_history(self):
        # Тестируем историю поиска для неавторизованного пользователя
        self.client.logout()  # Удаляем аутентификацию
        response = self.client.get('/api/v1/analytics/search-history/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Изменено на 401
        self.assertEqual(response.data['detail'], 'Для просмотра истории поиска необходимо авторизоваться.')
