from .base import *

DEBUG = False

ALLOWED_HOSTS = ['your-production-domain.com']


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'your_db_name',
#         'USER': 'your_db_user',
#         'PASSWORD': 'your_db_password',
#         'HOST': 'your_db_host',
#         'PORT': 'your_db_port',
#     }
# }

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(PARENT_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(PARENT_DIR, "static")]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PARENT_DIR, 'media')



EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = config("EMAIL_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_PASSWORD")

# DEFAULT_FROM_EMAIL = 'example@example.com'

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

CORS_ALLOWED_ORIGINS = [
    "https://example.com",
]