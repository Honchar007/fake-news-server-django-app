# settings.py
import sys
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&f*p!bek1*4erj@wd+h5bsl2(zy$*kt+x4l@)_z%i&9h5*w^q0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']  # For development only

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fakenews_server',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Must be at the top
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Simplified CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True  # For development only
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'djangoProject1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'djangoProject1.wsgi.application'

DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fakenews_db',
        'USER': 'fakenewsuser',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': '',
    }
}


if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    }

if 'test' in sys.argv:
    class MockModel:
        def __init__(self):
            self.name = 'mock_model'

        def predict(self, texts):
            return [1 for _ in texts]

        def predict_proba(self, texts):
            return [[0.2, 0.8] for _ in texts]

        def classify_text(self, text):
            return {'label': 'FAKE', 'score': 0.8}

        def get_probabilities(self, text):
            return [0.2, 0.8]


    MOCK_MODELS = {
        'rf': MockModel(),
        'bert': MockModel(),
        'lr': MockModel(),
        'nb': MockModel(),
        'svm': MockModel(),
        'mlp': MockModel(),
    }


    def mock_load_model(model_name):
        if model_name not in MOCK_MODELS:
            raise ValueError(f"Invalid model name: {model_name}")
        return MOCK_MODELS[model_name]


    import fakenews_server.ml_models

    fakenews_server.ml_models.load_model = mock_load_model

# settings.py
if 'test' in sys.argv:
    # Mock ML model functionality during tests
    class MockModel:
        def predict(self, features):
            return [1]

        def predict_proba(self, features):
            return [[0.2, 0.8]]


    MOCK_PIPELINE = lambda **kwargs: lambda x: [{'label': 'FAKE', 'score': 0.8}]

    # Mock the imports used by ml_models.py
    import sys
    import mock

    sys.modules['joblib'] = mock.MagicMock()
    sys.modules['joblib'].load = lambda x: MockModel()

    sys.modules['transformers'] = mock.MagicMock()
    sys.modules['transformers'].pipeline = MOCK_PIPELINE

if 'test' in sys.argv:
    class MockModel:
        def predict(self, features):
            """Always return single prediction regardless of input size"""
            return [1]

        def predict_proba(self, features):
            """Always return single probability pair"""
            return [[0.2, 0.8]]


    # Mock for BERT pipeline
    def mock_pipeline(*args, **kwargs):
        def predict(text):
            return [{'label': 'FAKE', 'score': 0.8}]

        return predict


    # Mock the imports
    import sys
    import mock

    mock_joblib = mock.MagicMock()
    mock_joblib.load = lambda x: MockModel()
    sys.modules['joblib'] = mock_joblib

    mock_transformers = mock.MagicMock()
    mock_transformers.pipeline = mock_pipeline
    sys.modules['transformers'] = mock_transformers

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

