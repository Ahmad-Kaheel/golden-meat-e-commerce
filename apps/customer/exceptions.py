from django.utils.translation import gettext as _
from rest_framework.exceptions import APIException


class AccountDisabledException(APIException):
    status_code = 403
    default_detail = _("User account is disabled.")
    default_code = "account-disabled"


class InvalidCredentialsException(APIException):
    status_code = 401
    default_detail = _("Wrong email or password.")
    default_code = "invalid-credentials"
