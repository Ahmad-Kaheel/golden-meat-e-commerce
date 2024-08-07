from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView
from rest_framework.response import Response
from rest_framework import permissions, status

from django.utils.translation import gettext_lazy as _

from customer.serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
)


class UserRegisterationAPIView(RegisterView):
    """
    Register new users using or email and password.
    """

    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        response_data = ""

        email = request.data.get("email", None)

        if email:
            response_data = {"detail": _("Verification e-mail sent.")}

        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class UserLoginAPIView(LoginView):
    """
    Authenticate existing users using email and password.
    """

    serializer_class = UserLoginSerializer