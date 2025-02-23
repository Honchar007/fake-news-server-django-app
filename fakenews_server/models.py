# models.py
from django.contrib.auth.models import User
from django.db import models

class NewsCheckHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='check_history')
    news_title = models.CharField(max_length=255)
    news_text = models.TextField()
    model_used = models.CharField(max_length=100)  # Model name, e.g., 'MLP', 'Random Forest'
    prediction = models.CharField(max_length=10)  # 'Real' or 'Fake'
    check_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} checked {self.news_title}"