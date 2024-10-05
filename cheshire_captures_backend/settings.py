from pathlib import Path
import os
import re
import dj_database_url
import logging

# Load environment variables from env.py if it exists
if os.path.exists('env.py'):
    import env

BASE_DIR = Path(__file__).resolve().parent.parent

# Secret and Security Settings
SECRET_KEY = os.environ.get('SECRET_KEY', '')
DEBUG = False

ALLOWED_HOSTS = [
    os.environ.get('ALLOWED_HOST'),
    '127.0.0.1',
    'localhost',
    '*.gitpod.io',
    'cheshire-captures-4a500dc7ab0a.herokuapp.com',
    '8000-nickcmoore-cheshirecapt-1t388js0qvn.ws-eu116.gitpod.io',
]

# Logging configuration for DisallowedHost errors
logger = logging.getLogger('django.security.DisallowedHost')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.WARNING)

# Cloudinary Configuration
CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL', '')
if CLOUDINARY_URL:
    CLOUDINARY_STORAGE = {'CLOUDINARY_URL': CLOUDINARY_URL}
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
else:
    CLOUDINARY_STORAGE = {}

MEDIA_URL = '/media/'

# Application Definitions
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
    'django.contrib.sites',
    'django_filters',
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
    'corsheaders',
]

# Authentication and JWT Settings
SITE_ID = 1
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [(
        'rest_framework.authentication.SessionAuthentication'
        if 'DEV' in os.environ
        else 'dj_rest_auth.jwt_auth.JWTCookieAuthentication'
    )]
}

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'cheshire_captures_backend.serializers.CurrentUserSerializer'
}


REST_USE_JWT = True
JWT_AUTH_SECURE = True
JWT_AUTH_COOKIE = 'cheshire-captures-auth'
JWT_AUTH_REFRESH_COOKIE = 'cheshire-captures-refresh'

# Middleware Definitions
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]


# URL Configuration
ROOT_URLCONF = 'cheshire_captures_backend.urls'
WSGI_APPLICATION = 'cheshire_captures_backend.wsgi.application'

# Database Configuration
DATABASES = {
    'default': dj_database_url.parse(os.environ.get("DATABASE_URL")) if 'DEV' not in os.environ else {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static and Media Files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Templates Configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'cheshire_captures_backend/templates'],
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

# Auto Field Settings
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
