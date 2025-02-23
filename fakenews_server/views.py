from django.shortcuts import render, redirect

from django.contrib.auth.models import User

from fakenews_server.transform_data import preprocess_input
from fakenews_server.ml_models import load_model  # Assuming you have a function to load your models

from django.contrib.auth import login
from .forms import UserRegistrationForm

from .models import NewsCheckHistory
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer, NewsPredictionSerializer, \
    UserRecoverySerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  # Automatically log in the new user
            return redirect('home')  # Redirect to a homepage or dashboard
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def predict_news(request):
    serializer = NewsPredictionSerializer(data=request.data)

    if serializer.is_valid():
        title = serializer.validated_data['title']
        text = serializer.validated_data['text']
        model_name = serializer.validated_data['model_name']

        try:
            # Load the specified model
            model = load_model(model_name)

            if model_name == 'bert':
                # For BERT, combine title and text without vectorization
                combined_text = f"{title} [SEP] {text}"
                features = combined_text
            else:
                # For traditional models, use the existing preprocessing
                features = preprocess_input(title, text)

            # Make prediction
            prediction_result = model.predict([features])[0]
            prediction = "FAKE" if prediction_result == 1 else "REAL"

            # Get confidence if available
            confidence = None
            if hasattr(model, 'predict_proba'):
                try:
                    proba = model.predict_proba([features])[0]
                    confidence = float(proba[1])  # Probability of being fake
                except Exception as e:
                    print(f"Failed to get probability: {str(e)}")
                    pass

            # Save the prediction history
            history = NewsCheckHistory.objects.create(
                user=request.user,
                news_title=title,
                news_text=text,
                model_used=model_name,
                prediction=prediction
            )

            response_data = {
                'prediction': prediction,
                'model_used': model_name,
                'title': title,
                'confidence': f"{confidence:.2%}" if confidence is not None else None
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': f'Prediction failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def user_history(request):
    history = NewsCheckHistory.objects.filter(user=request.user).order_by('-check_date')
    history_list = list(history.values())
    return Response(history_list, status=status.HTTP_200_OK)

# Registration view
class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login view with JWT
class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                # Retrieve the user by email
                user = User.objects.get(email=email)
                # Authenticate user by email and password
                user = authenticate(username=user.username, password=password)
                if user:
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def recover_user(request):
    """
    Endpoint to recover user information from token
    Returns id, username, and email of the authenticated user
    """
    try:
        serializer = UserRecoverySerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': f'Failed to recover user information: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
