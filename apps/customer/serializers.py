from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _

from customer.exceptions import (
    AccountDisabledException,
    InvalidCredentialsException,
)
from customer.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationSerializer(RegisterSerializer):
    """
    Serializer for registrating new users using email or phone number in future.
    """
    email = serializers.EmailField(required=True)
    username = None
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)

    def validate(self, validated_data):
        email = validated_data.get("email")

        if not (email):
            raise serializers.ValidationError(_("Enter an email."))

        if validated_data["password1"] != validated_data["password2"]:
            raise serializers.ValidationError(
                _("The two password fields didn't match.")
            )
        return validated_data
    
    def save(self, request):
        user = super().save(request)
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer to login users with email.
    """

    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def _validate_email(self, email, password):
        user = None

        if email and password:
            user = authenticate(username=email, password=password)
        else:
            raise serializers.ValidationError(
                _("Enter your email and password.")
            )

        return user

    def validate(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")

        user = None

        user = self._validate_email(email, password)

        if not user:
            raise InvalidCredentialsException()

        if not user.is_active:
            raise AccountDisabledException()

        if email:
            email_address = user.emailaddress_set.filter(
                email=user.email, verified=True
            ).exists()
            if not email_address:
                raise serializers.ValidationError(_("E-mail is not verified."))

        validated_data["user"] = user
        return validated_data


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize the user Profile model
    """

    class Meta:
        model = Profile
        fields = (
            "avatar",
            "bio",
            "created_at",
            "updated_at",
        )


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class to seralize User model
    """

    profile = ProfileSerializer(read_only=True)
    # addresses = AddressReadOnlySerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "profile",
            # "addresses",
        )