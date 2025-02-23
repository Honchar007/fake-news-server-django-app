from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

class MiddlewareTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_cors_headers(self):
        """Test CORS headers are present"""
        response = self.client.options(
            reverse('login'),
            HTTP_ORIGIN='http://localhost:3000'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Access-Control-Allow-Origin', response.headers)
        self.assertIn('Access-Control-Allow-Methods', response.headers)
        