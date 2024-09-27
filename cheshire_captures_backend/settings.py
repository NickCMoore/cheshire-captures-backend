from pathlib import Path
import os
import dj_database_url
import re

# Load environment variables from env.py if it exists
if os.path.exists('env.py'):
    import env

# Cloudinary Configuration
CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL', '')
if CLOUDINARY_URL:
    CLOUDINARY_STORAGE = {
        'CLOUDINARY_URL': CLOUDINARY_URL
    }
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
else:
    CLOUDINARY_STORAGE = {}

MEDIA_URL = '/media/'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

if not SECRET_KEY:
    raise ImproperlyConfigured("The SECRET_KEY setting must not be empty.")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

import logging

logger = logging.getLogger('django.security.DisallowedHost')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '*.gitpod.io', 
    '8000-nickcmoore-cheshirecapt-1t388js0qvn.ws-eu116.gitpod.io',
    'https://cheshire-captures-backend-084aac6d9023.herokuapp.com', 
]


# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = [
    'https://8000-nickcmoore-cheshirecapt-1t388js0qvn.ws-eu116.gitpod.io',  
    'https://*.gitpod.io', 
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'django_filters',
    'corsheaders',
    'cloudinary_storage',
    'cloudinary',
    'photographers',
    'allauth', 
    'allauth.account',  
    'allauth.socialaccount',  
    'dj_rest_auth.registration',
    'drf_yasg',
    'photo',
    'messaging',
]

SITE_ID = 1

# Authentication Backends
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  
    'allauth.account.auth_backends.AuthenticationBackend',
)

# AllAuth Settings
ACCOUNT_EMAIL_REQUIRED = True  
ACCOUNT_AUTHENTICATION_METHOD = 'username'  
ACCOUNT_EMAIL_VERIFICATION = 'optional' 
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True 
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ],
}


REST_USE_JWT = True
JWT_AUTH_SECURE = True
JWT_AUTH_COOKIE = 'cheshire-captures-auth'
JWT_AUTH_REFRESH_COOKIE = 'cheshire-captures-refresh'
JWT_AUTH_SAMESITE = 'None'

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'drf_api.serializers.CurrentUserSerializer'
}

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER') 
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

if 'CLIENT_ORIGIN_DEV' in os.environ:
    extracted_url = re.match(r'^.+-', os.environ.get('CLIENT_ORIGIN_DEV', ''), re.IGNORECASE).group(0)
    CORS_ALLOWED_ORIGIN_REGEXES = [
        rf"{extracted_url}(eu|us)\d+\w\.gitpod\.io$",
    ]

CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'cheshire_captures_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'cheshire_captures_backend.wsgi.application'

# Database configuration
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
db_url = os.environ.get("DATABASE_URL")
if db_url:
    DATABASES = {
        'default': dj_database_url.parse(db_url)
    }
    print('Connected to PostgreSQL database')
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    print('Using SQLite database')


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
