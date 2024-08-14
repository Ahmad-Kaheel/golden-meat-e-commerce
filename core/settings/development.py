import os
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = config("DEBUG", default=False, cast=bool)
DEBUG = True

# ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())
ALLOWED_HOSTS = []


REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += (
    'rest_framework.authentication.SessionAuthentication',
)


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "../", "mediafiles")

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "../", "staticfiles")


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'example@example.com'

CORS_ORIGIN_ALLOW_ALL = True