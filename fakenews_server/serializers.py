# serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import NewsCheckHistory

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

# Add this new serializer
class NewsPredictionSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    text = serializers.CharField(required=True)
    model_name = serializers.ChoiceField(
        choices=[
            ('rf', 'Random Forest'),
            ('lr', 'Logistic Regression'),
            ('nb', 'Naive Bayes'),
            ('mlp', 'Multi-layer Perceptron'),
            ('svm', 'Support Vector Machine'),
            ('bert', 'BERT Model')
        ],
        required=True
    )

class NewsHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCheckHistory
        fields = ['news_title', 'news_text', 'model_used', 'prediction', 'check_date']
        read_only_fields = ['check_date']

class UserRecoverySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id', 'username', 'email']
