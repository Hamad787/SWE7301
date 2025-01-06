from pathlib import Path
from datetime import timedelta
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-j*gn1-^_ik3ag^q=d2bwq7yce-v@(k$y6^%y+&e97v$dplv!i0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'frontend',
    'rest_framework',
    'rest_framework_simplejwt',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Flask API Configuration
FLASK_API = {
    'BASE_URL': 'http://127.0.0.1:5000',  # Base URL without /api
    'TIMEOUT': 30,
    'ENDPOINTS': {
        # Products
        'PRODUCTS': '/api/products',  # List/Create
        'PRODUCT_DETAIL': '/api/products/{}',  # Get/Update/Delete
        
        # Orders
        'ORDERS': '/api/orders',  # List/Create
        'ORDER_DETAIL': '/api/orders/{}',  # Get/Update/Delete
        
        # Payment
        'PAYMENT': '/api/payment',  # Base payment endpoint
        'PROCESS_PAYMENT': '/api/payment/process/{}',  # Process payment
        'ORDER_PAYMENT': '/api/payment/order/{}',  # Process order payment
        
        # Auth
        'AUTH': '/api/auth/login',  # Login
        'LOGIN': '/api/auth/login',  # Same as AUTH
        'REGISTER': '/api/auth/register',  # Register
        
        # Data
        'MEASUREMENTS': '/api/data'  # Measurement data
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler'
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'USER_ID_FIELD': 'username',  
    'USER_ID_CLAIM': 'sub',  
}

ROOT_URLCONF = 'roundsphere_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'frontend/templates',  
        ],
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


WSGI_APPLICATION = 'roundsphere_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# PayPal Settings
PAYPAL_CLIENT_ID = 'AcOpRKwGfjd52X_NHgh3k2TkTTlBJhyvoFp3kCI2Iu4E8XQdHqkTblyKrCh0Fpt5mun2kh5GFKSaG2G_'
PAYPAL_SECRET = 'EEDynQbuBAvCNTe8_IUlZ1JWIdFMuiuiCCVPrFQN-2QLUUPzlYPzxespnU8hjJc7RXjqJqo30pYj_orT'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
