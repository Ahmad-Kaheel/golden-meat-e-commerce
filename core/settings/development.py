import os
from .base import *
from django.utils.translation import gettext_lazy as _


DEBUG = True


ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '206.81.22.164']


REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += (
    'rest_framework.authentication.SessionAuthentication',
)


STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(PARENT_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(PARENT_DIR, "static")]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PARENT_DIR, 'media')



EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'example@example.com'



CORS_ORIGIN_ALLOW_ALL = True

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'mydatabase', 
#         'USER': 'myuser',
#         'PASSWORD': '',
#         'HOST': "db",
#         'PORT': "5432",
#         'OPTIONS': {
#             'service': 'db',
#         }
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(PARENT_DIR, "db.sqlite3"),
    }
}



###################################  register and login  ###################################


"""
{
  "email": "customer@example.com",
  "password1": "CustomerPassword123",
  "password2": "CustomerPassword123",
  "is_vendor": false,
  "first_name": "Alice",
  "last_name": "Smith",
  "gender": "female",
  "date_of_birth": "1990-05-20",
  "phone_number": "+1987654321"
}


{
  "email": "vendor@example.com",
  "password1": "SecurePassword123",
  "password2": "SecurePassword123",
  "is_vendor": true,
  "company_name": "ABC Trading Co.",
  "company_type": "Retailer",
  "commercial_registration_number": "123456789",
  "tax_number": "987654321",
  "manager_name": "John Doe",
  "company_email": "contact@abctrading.com",
  "mobile_number": "+1234567890",
  "website": "https://www.abctrading.com",
  "business_activity": "Wholesale electronics"
}


"""

"""

{
  "email": "customer@example.com",
  "password": "CustomerPassword123"
}


{
  "email": "vendor@example.com",
  "password": "SecurePassword123"
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