from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _

from address.serializers import ShippingAddressSerializer, BillingAddressSerializer
from customer.exceptions import (
    AccountDisabledException,
    InvalidCredentialsException,
)
from customer.models import Profile

User = get_user_model()


class UserRegistrationSerializer(RegisterSerializer):
    """
    Serializer for registrating new users using email or phone number in future.
    """
    email = serializers.EmailField(required=True)
    username = None

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
    shipping_address = ShippingAddressSerializer(many=True, read_only=True, source='user.shipping_addresses')
    billing_address = BillingAddressSerializer(many=True, read_only=True, source='user.billing_addresses')
    avatar = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Profile
        fields = (
            "first_name", "last_name", "avatar",
            "shipping_address", "billing_address",
            "bio", "created_at", "updated_at",
        )

    def clean_text_field(self, value):
        return value.strip() if value else None

    def validate(self, data):
        # Clean and validate fields without considering the language
        data['first_name'] = self.clean_text_field(data.get('first_name'))
        data['last_name'] = self.clean_text_field(data.get('last_name'))
        data['bio'] = self.clean_text_field(data.get('bio'))
        
        return data
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Set the default representation without language-specific logic
        representation['first_name'] = instance.first_name
        representation['last_name'] = instance.last_name
        representation['bio'] = instance.bio

        return representation


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class to seralize User model
    """

    profile = ProfileSerializer(read_only=True)
    shipping_address = ShippingAddressSerializer(read_only=True, many=True)
    billing_address = BillingAddressSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "is_active",
            "profile",
            "shipping_address",
            "billing_address",
        )