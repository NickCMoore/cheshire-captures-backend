from pathlib import Path
import os
import re
import dj_database_url
import logging

# Load environment variables from env.py if it exists
if os.path.exists('env.py'):
    import env

# Base directory path
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key and Debug mode
SECRET_KEY = os.environ.get('SECRET_KEY', '')
DEBUG = 'DEV' in os.environ

# Automatically add Gitpod URLs to ALLOWED_HOSTS
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '*.gitpod.io',
    'https://cheshire-captures-backend-084aac6d9023.herokuapp.com',
    '8000-nickcmoore-cheshirecapt-9zo58vdqbuc.ws-eu116.gitpod.io',
]

if 'GITPOD_WORKSPACE_URL' in os.environ:
    gitpod_url = os.environ['GITPOD_WORKSPACE_URL']
    host = re.sub(r'^https://', '', gitpod_url)
    ALLOWED_HOSTS.append(host)

# Logging for DisallowedHost errors
logger = logging.getLogger('django.security.DisallowedHost')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.WARNING)

# Cloudinary Configuration for media storage
CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL', '')
if CLOUDINARY_URL:
    CLOUDINARY_STORAGE = {'CLOUDINARY_URL': CLOUDINARY_URL}
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
else:
    CLOUDINARY_STORAGE = {}

MEDIA_URL = '/media/'

# Installed apps
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

# Language and timezone settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

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
    )],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DATETIME_FORMAT': '%d %b %Y',
}

# JSON-only rendering in production
if 'DEV' not in os.environ:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
        'rest_framework.renderers.JSONRenderer',
    ]

REST_USE_JWT = True
JWT_AUTH_SECURE = True
JWT_AUTH_COOKIE = 'cheshire-captures-auth'
JWT_AUTH_REFRESH_COOKIE = 'cheshire-captures-refresh'
JWT_AUTH_SAMESITE = 'None'

# Custom user serializer for dj-rest-auth
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'cheshire_captures_backend.serializers.CurrentUserSerializer'
}

# Middleware settings
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

# CORS Configuration
CORS_ALLOW_CREDENTIALS = True

# Regex to allow all Gitpod subdomains dynamically
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://\d{4,5}-\w+-\w+-\w+-\w+\.ws-eu\d+\.gitpod\.io$",
]

# Production CORS origin
CORS_ALLOWED_ORIGINS = [
    'https://cheshire-captures-4a500dc7ab0a.herokuapp.com',
]

# URL Configuration
ROOT_URLCONF = 'cheshire_captures_backend.urls'
WSGI_APPLICATION = 'cheshire_captures_backend.wsgi.application'

# Database configuration
if 'DEV' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
    }
    print('connected')

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Static and media files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Templates settings
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
