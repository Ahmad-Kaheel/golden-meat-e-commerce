from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured

from customer.utils import normalise_email

User = get_user_model()


class EmailAuthBackend(ModelBackend):
    """
    Custom authentication backend to login users using email address.
    """

    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return
        except User.DoesNotExist:
            return

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        
# if hasattr(User, "REQUIRED_FIELDS"):
#     if not (User.USERNAME_FIELD == "email" or "email" in User.REQUIRED_FIELDS):
#         raise ImproperlyConfigured(
#             "EmailBackend: Your User model must have an email field with blank=False"
#         )

# class EmailAuthBackend(ModelBackend):
#     """
#     Custom authentication backend to login users using email address.
#     """
#     def _authenticate(self, request, email=None, password=None, *args, **kwargs):
#         if email is None:
#             if "username" not in kwargs or kwargs["username"] is None:
#                 return None
#             clean_email = normalise_email(kwargs["username"])
#         else:
#             clean_email = normalise_email(email)

#         # Check if we're dealing with an email address
#         if "@" not in clean_email:
#             return None
#         matching_users = User.objects.filter(email__iexact=clean_email)
#         authenticated_users = [
#             user
#             for user in matching_users
#             if (user.check_password(password) and self.user_can_authenticate(user))
#         ]
#         if len(authenticated_users) == 1:
#             # Happy path
#             return authenticated_users[0]
#         elif len(authenticated_users) > 1:
#             # This is the problem scenario where we have multiple users with
#             # the same email address AND password. We can't safely authenticate
#             # either.
#             raise User.MultipleObjectsReturned(
#                 "There are multiple users with the given email address and password"
#             )
#         return None

#     def authenticate(self, *args, **kwargs):
#         return self._authenticate(*args, **kwargs)
