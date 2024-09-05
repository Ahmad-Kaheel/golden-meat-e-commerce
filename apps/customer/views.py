from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView
from drf_spectacular.utils import(
    extend_schema, extend_schema_view, 
    OpenApiParameter, OpenApiExample
)
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.generics import (
    RetrieveUpdateAPIView,
    RetrieveAPIView,
)
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language

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


common_parameters = [
    OpenApiParameter(
        name='Accept-Language',
        location=OpenApiParameter.HEADER,
        description=_('Specify the language code for the response content. Supported values are "en" for English and "ar" for Arabic.'),
        required=False,
        type=str,
        examples=[
            OpenApiExample("English", value="en"),
            OpenApiExample("Arabic", value="ar")
        ]
    ),
]


@extend_schema(
    tags=['User Management'],
    summary='User Registration',
    description='Register new users using email and password. Returns a message indicating whether a verification email has been sent.',
    request=UserRegistrationSerializer,
    parameters=common_parameters,
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
    parameters=common_parameters,
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
        parameters=common_parameters,
        responses={200: ProfileSerializer},
    ),
    put=extend_schema(
        tags=['User Profile'],
        summary='Update User Profile',
        description=(
            'Update the profile information of the authenticated user. '
            'To update the `avatar`, send the image as a file in the multipart/form-data request. '
            'Other fields can be sent as part of the same request. '
            'For example, to update the profile, use the following format:'
            '\n\n'
            '```\n'
            'curl -X PUT \\\n'
            '  http://127.0.0.1:8000/api/user/profile/ \\\n'
            '  -H "accept: application/json" \\\n'
            '  -H "Authorization: Bearer YOUR_TOKEN" \\\n'
            '  -F "bio_ar=الوصف الاول" \\\n'
            '  -F "avatar=@C:/Users/tyu/Desktop/restu10.PNG" \\\n'
            '  -F "first_name_ar=امين1" \\\n'
            '  -F "last_name_ar=امين1"\n'
            '```'
            '\n\n'
            'Note that the request should be sent using `multipart/form-data` and not `application/json`.'
        ),
        responses={200: ProfileSerializer},
        parameters=common_parameters,
    ),
    patch=extend_schema(
        tags=['User Profile'],
        summary='Partially Update User Profile',
        description='Partially update the profile information of the authenticated user.',
        request=ProfileSerializer,
        responses={200: ProfileSerializer},
        parameters=common_parameters,
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
        return self.request.user.profile

    def get_queryset(self):
        user = self.request.user
        language = get_language()
        
        # You can filter or modify the queryset based on the current language if needed
        if language == 'ar':
            return Profile.objects.filter(user=user, bio_ar__isnull=False)
        else:
            return Profile.objects.filter(user=user)



@extend_schema(
    tags=['User Management'],
    summary='Retrieve User Details',
    description='Fetch the details of the authenticated user.',
    parameters=common_parameters,
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