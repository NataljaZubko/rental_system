from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.listings.models import Listing
from apps.users.models import User

class ListingAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='landlord@example.com',
            password='testpassword',
            position='LANDLORD'
        )
        self.client.force_authenticate(user=self.user)

        self.listing_data = {
            'title': 'Test Listing',
            'description': 'A beautiful apartment',
            'location': 'Berlin',
            'price': '1500.00',
            'rooms': 2,
            'housing_type': 'APARTMENT'
        }

    def test_create_listing(self):
        response = self.client.post('/api/v1/listings/', self.listing_data)
        print("Create Listing Response Data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_listings(self):
        # Создаем объявление
        self.client.post('/api/v1/listings/', self.listing_data)
        response = self.client.get('/api/v1/listings/')
        print("Get Listings Response Data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_update_listing(self):
        # Создаем объявление
        response = self.client.post('/api/v1/listings/', self.listing_data)
        listing_id = response.data['id']

        # Обновляем объявление
        update_data = {'title': 'Updated Listing'}
        response = self.client.patch(f'/api/v1/listings/{listing_id}/', update_data)
        print("Update Listing Response Data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Listing')

    def test_delete_listing(self):
        # Создаем объявление
        response = self.client.post('/api/v1/listings/', self.listing_data)
        listing_id = response.data['id']

        # Удаляем объявление
        response = self.client.delete(f'/api/v1/listings/{listing_id}/')
        print("Delete Listing Response Status:", response.status_code)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)