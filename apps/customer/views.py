from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.generics import (
    RetrieveUpdateAPIView,
    RetrieveAPIView,
)
from django.utils.translation import gettext_lazy as _

from customer.permissions import IsNotAuthenticated, IsUserProfileOwner
from customer.serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    ProfileSerializer,
)
from customer.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()



@extend_schema(
    tags=['User Management'],
    summary='User Registration',
    description='Register new users using email and password. Returns a message indicating whether a verification email has been sent.',
    request=UserRegistrationSerializer,
)
class UserRegisterationAPIView(RegisterView):
    """
    Register new users using or email and password.
    """

    serializer_class = UserRegistrationSerializer
    permission_classes = [IsNotAuthenticated]

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


@extend_schema(
    tags=['User Management'],
    summary='User Login',
    description='Authenticate users using email and password. Returns access and refresh tokens along with user details upon successful authentication.',
    request=UserLoginSerializer,
)
class UserLoginAPIView(LoginView):
    """
    Authenticate existing users using email and password.
    """

    serializer_class = UserLoginSerializer


@extend_schema_view(
    get=extend_schema(
        tags=['User Profile'],
        summary='Retrieve User Profile',
        description='Fetch the profile details of the authenticated user.',
    ),
    put=extend_schema(
        tags=['User Profile'],
        summary='Update User Profile',
        description='Update the profile information of the authenticated user.',
        request=ProfileSerializer,
    ),
    patch=extend_schema(
        tags=['User Profile'],
        summary='Partially Update User Profile',
        description='Partially update the profile information of the authenticated user.',
        request=ProfileSerializer,
    ),
)
class ProfileAPIView(RetrieveUpdateAPIView):
    """
    Get, Update user profile
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsUserProfileOwner]

    def get_object(self):
        user = self.queryset.get(id=self.request.user.id)
        return user


@extend_schema(
    tags=['User Management'],
    summary='Retrieve User Details',
    description='Fetch the details of the authenticated user.',
)
class UserAPIView(RetrieveAPIView):
    """
    Get user details
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        user = self.queryset.get(id=self.request.user.id)
        return user