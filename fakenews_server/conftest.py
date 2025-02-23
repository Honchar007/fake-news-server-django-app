import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    def make_user(**kwargs):
        return get_user_model().objects.create_user(**kwargs)
    return make_user

@pytest.fixture
def auth_client(api_client, create_user):
    user = create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    response = api_client.post(
        reverse('login'),
        {
            'email': 'test@example.com',
            'password': 'testpass123'
        },
        format='json'
    )
    api_client.credentials(
        HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}'
    )
    return api_client
