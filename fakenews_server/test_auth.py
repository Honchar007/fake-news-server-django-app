from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.User = get_user_model()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        self.user = self.User.objects.create_user(**self.user_data)

    def test_user_registration(self):
        """Test user registration endpoint"""
        new_user_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123'
        }
        response = self.client.post(
            reverse('register'),
            new_user_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            self.User.objects.filter(email='new@example.com').exists()
        )

    def test_user_login(self):
        """Test user login endpoint"""
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post(
            reverse('login'),
            login_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_refresh(self):
        """Test token refresh endpoint"""
        # First login to get tokens
        login_response = self.client.post(
            reverse('login'),
            {
                'email': self.user_data['email'],
                'password': self.user_data['password']
            },
            format='json'
        )
        refresh_token = login_response.data['refresh']

        # Try to refresh token
        response = self.client.post(
            reverse('token_refresh'),
            {'refresh': refresh_token},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_invalid_login(self):
        """Test invalid login credentials"""
        invalid_data = {
            'email': self.user_data['email'],
            'password': 'wrongpass'
        }
        response = self.client.post(
            reverse('login'),
            invalid_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
