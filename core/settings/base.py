
import os
import sys
from pathlib import Path
from datetime import timedelta
from decouple import Csv, config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PARENT_DIR = BASE_DIR.parent
sys.path.append(str(PARENT_DIR / 'apps'))
# print("BASE_DIR", BASE_DIR)


# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = config("SECRET_KEY")
SECRET_KEY = "fffffffffffdddddddddssssss$#AAAAsdfsdf123224gfffffd"



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.sites",
    # Third party apps
    "rest_framework",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth.registration",
    "phonenumber_field",
    "corsheaders",
    'drf_spectacular',
    # local app
    "customer",
    "address",
    "catalogue",
    # "order",
    "voucher",
    # "basket",

]

SITE_ID = 1
CORS_ALLOW_CREDENTIALS = True

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'





# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'mydatabase', 
#         'USER': 'myuser',
#         'PASSWORD': 'mypassword',
#         'HOST': "db",
#         'PORT': "5432",
#     }
# }

DB_ENGINE = config("DB_ENGINE", default="django.db.backends.sqlite3")
DB_NAME = config("DB_NAME", default=os.path.join(BASE_DIR, "db.sqlite3"))
DB_USER = config("DB_USERNAME", default="")
DB_PASSWORD = config("DB_PASSWORD", default="")
DB_HOST = config("DB_HOSTNAME", default="")
DB_PORT = config("DB_PORT", default="")

# # إعداد قاعدة البيانات
# if DB_ENGINE == "django.db.backends.postgresql" and all([DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT]):
#     DATABASES = {
#         "default": {
#             "ENGINE": DB_ENGINE,
#             "NAME": DB_NAME,
#             "USER": DB_USER,
#             "PASSWORD": DB_PASSWORD,
#             "HOST": DB_HOST,
#             "PORT": DB_PORT,
#         }
#     }
# else:
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.sqlite3",
#             "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
#         }
#     }

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('en-us', 'English'),
    ('ar', 'Arabic'),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



# Authentication

AUTHENTICATION_BACKENDS = [
    "customer.backends.email_backend.EmailAuthBackend",
]

# user model
AUTH_USER_MODEL = 'customer.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
}

REST_USE_JWT = True

# auth cookie keys
JWT_AUTH_COOKIE = "email-auth"
JWT_AUTH_REFRESH_COOKIE = "email-refresh-token"

# ACCOUNT_EMAIL_VERIFICATION SETTINGS
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
USER_MODEL_USERNAME_FIELD = 'email'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=40),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

MEDIA_URL = '/media/'

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


SPECTACULAR_SETTINGS = {
    'TITLE': 'Your API',
    'DESCRIPTION': 'API description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SECURITY': [
        {
            'BearerAuth': []
        }
    ],
    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,
    },
}



# login
"""

{
	"email": "amin1@amin.com",
	"password": "123qweasd_"
}


"""

"""
{
    "email": "amin1@amin.com",
    "password1": "123qweasd_",
    "password2": "123qweasd_",
    "first_name": "amin1",
    "last_name": "amin1"
}

"""


# address
"""
{
  "city": "city1",
  "street_address": "street1",
  "apartment_address": "apartment1",
  "postal_code": "postal1",
  "is_default_for_billing": true,
  "is_default_for_shipping": true,
  "phone_number": "0099000990",
  "notes": "ssssddddfff"
}
"""