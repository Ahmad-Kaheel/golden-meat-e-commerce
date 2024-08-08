# core/settings/development.py

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += (
    'rest_framework.authentication.SessionAuthentication',
)

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

MEDIA_ROOT = BASE_DIR / "mediafiles"

STATIC_ROOT = BASE_DIR / "staticfiles"

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'example@example.com'

CORS_ORIGIN_ALLOW_ALL = True