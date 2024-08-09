from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter, OpenApiResponse, extend_schema_view
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
    summary='User Registration',
    description='Register new users using email and password. Returns a message indicating whether a verification email has been sent.',
    request=UserRegistrationSerializer,
    responses={
        201: OpenApiResponse(
            description='Successful registration. Verification email sent.',
            response=UserRegistrationSerializer,
            examples=[
                OpenApiExample(
                    'Successful Registration',
                    summary='Example Response',
                    value={
                        "detail": "Verification e-mail sent."
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            description='Bad Request - Validation errors for the provided data.'
        ),
    },
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
    summary='User Login',
    description='Authenticate users using email and password. Returns access and refresh tokens along with user details upon successful authentication.',
    request=UserLoginSerializer,
    responses={
        200: OpenApiResponse(
            description='Successful authentication. Access and refresh tokens are returned along with user details.',
            response=UserLoginSerializer,
            examples=[
                OpenApiExample(
                    'Successful Login',
                    summary='Example Response',
                    value={
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "user": {
                            "id": 1,
                            "email": "user@example.com",
                            "first_name": "John",
                            "last_name": "Doe",
                            "is_active": True
                        }
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            description='Bad Request - Invalid credentials provided.'
        ),
        401: OpenApiResponse(
            description='Unauthorized - Authentication failed.'
        ),
    },
)
class UserLoginAPIView(LoginView):
    """
    Authenticate existing users using email and password.
    """

    serializer_class = UserLoginSerializer


@extend_schema_view(
    get=extend_schema(
        summary='Retrieve User Profile',
        description='Fetch the profile details of the authenticated user.',
        responses={
            200: ProfileSerializer,
            401: OpenApiResponse(
                description='Unauthorized - Invalid or missing access token.'
            ),
        },
    ),
    put=extend_schema(
        summary='Update User Profile',
        description='Update the profile information of the authenticated user.',
        request=ProfileSerializer,
        responses={
            200: ProfileSerializer,
            400: OpenApiResponse(
                description='Bad Request - Invalid data provided.'
            ),
            401: OpenApiResponse(
                description='Unauthorized - Invalid or missing access token.'
            ),
            403: OpenApiResponse(
                description='Forbidden - User does not have permission to update this profile.'
            ),
        },
    ),
    patch=extend_schema(
        summary='Partially Update User Profile',
        description='Partially update the profile information of the authenticated user.',
        request=ProfileSerializer,
        responses={
            200: ProfileSerializer,
            400: OpenApiResponse(
                description='Bad Request - Invalid data provided.'
            ),
            401: OpenApiResponse(
                description='Unauthorized - Invalid or missing access token.'
            ),
            403: OpenApiResponse(
                description='Forbidden - User does not have permission to update this profile.'
            ),
        },
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


@extend_schema_view(
    get=extend_schema(
        summary='Retrieve User Details',
        description='Fetch the details of the authenticated user.',
        responses={
            200: UserSerializer,
            401: OpenApiResponse(
                description='Unauthorized - Invalid or missing access token.'
            ),
        },
    )
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