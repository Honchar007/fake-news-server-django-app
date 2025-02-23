from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from fakenews_server.models import NewsCheckHistory


class NewsPredictionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        # Get auth token
        response = self.client.post(
            reverse('login'),
            {'email': 'test@example.com', 'password': 'testpass123'},
            format='json'
        )
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_predict_news(self):
        """Test news prediction endpoint"""
        news_data = {
            'title': 'Test News',
            'text': 'This is test content',
            'model_name': 'bert'
        }
        response = self.client.post(
            reverse('predict_news'),  # Changed from 'predict' to 'predict_news'
            news_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('prediction', response.data)

    def test_get_prediction_history(self):
        """Test getting prediction history"""
        # Create some test history entries
        NewsCheckHistory.objects.create(
            user=self.user,
            news_title='Test News',
            news_text='Test content',
            model_used='bert',
            prediction='FAKE'
        )

        response = self.client.get(reverse('user_history'))  # Changed from 'history' to 'user_history'
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)

    def test_unauthorized_prediction(self):
        """Test prediction without authentication"""
        self.client.credentials()  # Remove auth credentials
        news_data = {
            'title': 'Test News',
            'text': 'Test content',
            'model_name': 'bert'
        }
        response = self.client.post(
            reverse('predict_news'),  # Changed from 'predict' to 'predict_news'
            news_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_prediction_with_invalid_data(self):
        """Test prediction with invalid data"""
        invalid_data = {
            'title': '',  # Empty title
            'text': 'Test content',
            'model_name': 'invalid_model'
        }
        response = self.client.post(
            reverse('predict_news'),
            invalid_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_history_with_multiple_entries(self):
        """Test history with multiple entries"""
        # Create multiple history entries
        entries = [
            {
                'news_title': f'Test News {i}',
                'news_text': f'Test content {i}',
                'model_used': 'bert',
                'prediction': 'FAKE'
            } for i in range(3)
        ]

        for entry in entries:
            NewsCheckHistory.objects.create(user=self.user, **entry)

        response = self.client.get(reverse('user_history'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)