from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.users.models import User

class UserAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.tenant_data = {
            'first_name': 'TenantFirstName',
            'last_name': 'TenantLastName',
            'email': 'tenant@example.com',
            'password': 'tenantpassword',
            'position': 'TENANT',
        }
        self.landlord_data = {
            'first_name': 'LandlordFirstName',
            'last_name': 'LandlordLastName',
            'email': 'landlord@example.com',
            'password': 'landlordpassword',
            'position': 'LANDLORD',
        }

        self.tenant = User.objects.create_user(
            first_name=self.tenant_data['first_name'],
            last_name=self.tenant_data['last_name'],
            email=self.tenant_data['email'],
            password=self.tenant_data['password'],
            position=self.tenant_data['position'],
        )

        self.landlord = User.objects.create_user(
            first_name=self.landlord_data['first_name'],
            last_name=self.landlord_data['last_name'],
            email=self.landlord_data['email'],
            password=self.landlord_data['password'],
            position=self.landlord_data['position'],
        )

    def test_user_registration(self):
        new_user_data = {
            'first_name': 'NewUserFirstName',
            'last_name': 'NewUserLastName',
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'position': 'LANDLORD',
        }
        response = self.client.post('/api/v1/users/register/', new_user_data)

        print("Registration Response Data:", response.data)
        print("Response Status Code:", response.status_code)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('email', response.data['user'])
        self.assertEqual(response.data['user']['email'], new_user_data['email'])

    def test_user_jwt_auth(self):
        response = self.client.post('/api/v1/users/login/', {
            'email': self.tenant_data['email'],
            'password': self.tenant_data['password']
        })

        print("JWT Auth Response Data:", response.data)
        print("Response Status Code:", response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_logout(self):
        response = self.client.post('/api/v1/users/login/', {
            'email': self.tenant_data['email'],
            'password': self.tenant_data['password']
        })
        access_token = response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        response = self.client.post('/api/v1/users/logout/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)