import os
from .base import *
from django.utils.translation import gettext_lazy as _


# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = config("DEBUG", default=False, cast=bool)
DEBUG = True


# ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += (
    # 'rest_framework.authentication.SessionAuthentication',
)


STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(PARENT_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(PARENT_DIR, "static")]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PARENT_DIR, 'media')



# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'example@example.com'
# Email service : mailtrap
EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_PORT = '2525'
EMAIL_HOST_USER = '4f4653374f7ae8'
EMAIL_HOST_PASSWORD = '0b0406b76e4d50'

CORS_ORIGIN_ALLOW_ALL = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mydatabase', 
        'USER': 'myuser',
        'PASSWORD': '',
        'HOST': "db",
        'PORT': "5432",
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": os.path.join(PARENT_DIR, "db.sqlite3"),
#     }
# }







###################################  register and login  ###################################


"""
{
    "email": "amin1@amin.com",
    "password1": "123qweasd_",
    "password2": "123qweasd_"
}

{
    "email": "amin2@amin.com",
    "password1": "123qweasd_",
    "password2": "123qweasd_"
}

"""

"""

{
	"email": "amin1@amin.com",
	"password": "123qweasd_"
}


{
	"email": "amin2@amin.com",
	"password": "123qweasd_"
}

"""
#################################  shipping and billing address  #################################

"""
# en shipping address
{
  "city": "cityshipping1",
  "street_address": "street_addressshipping1",
  "apartment_address": "apartment_addressshipping1",
  "postal_code": "postal2",
  "is_default_for_shipping": true,
  "phone_number": "+963968952711",
  "notes": "note1note1shipping1"
}

# ar shipping address
{
  "city": "المدينة الاولي الشحن الاول",
  "street_address": "الشارع الاول الشحن الاول",
  "apartment_address": "القسم الاول الشحن الاول",
  "postal_code": "postal1",
  "is_default_for_shipping": true,
  "phone_number": "+963968952711",
  "notes": "الملاحظة الاولى الشحن الاول"
}
"""



"""
# en billing1 address
{
  "city": "citybilling11",
  "street_address": "street_addressbilling11",
  "apartment_address": "apartment_addressbilling11",
  "postal_code": "postal1",
  "is_default_for_billing": true
}

# ar billing address
{
  "city": "المدينة الاولي الفاتورة الاولى",
  "street_address": "الشارع الاول الفاتورة الاولى",
  "apartment_address": "القسم الاول الفاتورة الاولى",
  "postal_code": "postal2",
  "is_default_for_billing": true
}
"""
#####################################    profile get update  ############################
"""
multipart/form-data
ar profile
{
  "bio_ar": "الوصف الاول",
  "avatar": "C:/Users/tyu/Desktop/restu10.PNG",
  "first_name_ar": "امين1",
  "last_name_ar": "امين1"
}

"""

"""
en profile
{
  "bio_en": "bio1 bio1",
  "avatar": "C:/Users/tyu/Desktop/restu10.PNG",
  "last_name_en": "amin1"
}


"""




################################## Review #################################
"""
en

{
  "product": 4,
  "rating": 5,
  "review": "review1review1review1review1review1"
}


{
  "product": 4,
  "rating": 5,
  "review": "الرد على  التعليق الاول",
  "parent": 6
}


"""





# checkout
"""

{
  "shipping_info": 52,
  "billing_info": 6,
  "payment_method": 2,
  "delivery_method": 1,
  "comment": "ordercommentordercommentordercommentordercommentordercomment"
}


"coupon_code": "E579B21C1A1FDCC8",

{
  "shipping_info": 52,
  "billing_info": 6,
  "payment_method": 2,
  "delivery_method": 1,
  "coupon": "E579B21C1A1FDCC8",
  "comment": "ordercommentordercommentordercommentordercommentordercomment"
}

"""