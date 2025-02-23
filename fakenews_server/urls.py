from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('predict/', views.predict_news, name='predict_news'),
    path('history/', views.user_history, name='user_history'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token endpoint

    path('login/', views.UserLoginView.as_view(), name='login'),
    path('recover-user/', views.recover_user, name='recover_user'),
]
