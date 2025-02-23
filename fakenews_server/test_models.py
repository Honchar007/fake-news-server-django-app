from django.test import TestCase
from django.contrib.auth import get_user_model
from fakenews_server.models import NewsCheckHistory

class ModelsTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_news_history_creation(self):
        """Test creating a news check history entry"""
        history = NewsCheckHistory.objects.create(
            user=self.user,
            news_title='Test News',
            news_text='Test content',
            model_used='bert',
            prediction='FAKE',
        )
        self.assertEqual(history.user.username, 'testuser')
        self.assertEqual(history.prediction, 'FAKE')

    def test_user_creation(self):
        """Test creating a custom user"""
        user = self.User.objects.create_user(
            username='newuser',
            email='new@example.com',
            password='newpass123'
        )
        self.assertEqual(user.email, 'new@example.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
