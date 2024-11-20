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
    Serializer for registering new users using email or phone number in future.
    """
    email = serializers.EmailField(required=True)
    is_vendor = serializers.BooleanField(required=False, default=False)
    # customer
    first_name = serializers.CharField(max_length=255, required=False)
    last_name = serializers.CharField(max_length=255, required=False)
    gender = serializers.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], required=False)
    date_of_birth = serializers.DateField(required=False)
    phone_number = serializers.CharField(max_length=15, required=False)
    # vendor
    company_name = serializers.CharField(required=False, allow_blank=True)
    company_type = serializers.CharField(required=False, allow_blank=True)
    commercial_registration_number = serializers.CharField(required=False, allow_blank=True)
    tax_number = serializers.CharField(required=False, allow_blank=True)
    manager_name = serializers.CharField(required=False, allow_blank=True)
    company_email = serializers.EmailField(required=False, allow_blank=True)
    mobile_number = serializers.CharField(required=False, allow_blank=True)
    website = serializers.URLField(required=False, allow_blank=True)
    business_activity = serializers.CharField(required=False, allow_blank=True)
    
    username = None

    def validate(self, validated_data):
        email = validated_data.get("email")
        is_vendor = validated_data.get("is_vendor", False)

        if not email:
            raise serializers.ValidationError(_("Enter an email."))

        if validated_data["password1"] != validated_data["password2"]:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        
        # Validation for normal users
        if not is_vendor:
            # Ensure that normal users provide their personal information
            if not all(field in validated_data and validated_data[field] for field in ["first_name", "last_name", "gender", "date_of_birth", "phone_number"]):
                raise serializers.ValidationError(_("Normal users must provide first name, last name, gender, date of birth, and phone number."))
            # Ensure vendors' fields are not provided
            if any(field in validated_data for field in [
                "company_name", "company_type", "commercial_registration_number", 
                "tax_number", "manager_name", "company_email", "mobile_number", 
                "website", "business_activity"
            ]):
                raise serializers.ValidationError(_("You cannot provide vendor details if you are not registering as a vendor."))
        
        # Validation for vendors
        if is_vendor:
            # Ensure vendors provide all required vendor fields
            required_fields = [
                "company_name", "company_type", "commercial_registration_number", 
                "tax_number", "manager_name", "company_email", "mobile_number", 
                "website", "business_activity"
            ]
            if not all(field in validated_data and validated_data[field] for field in required_fields):
                raise serializers.ValidationError(_("Vendor must provide all required vendor fields."))
            # Ensure personal details are not provided for vendors
            if any(field in validated_data for field in ["first_name", "last_name", "gender", "date_of_birth", "phone_number"]):
                raise serializers.ValidationError(_("Vendors should not provide personal information like first name, last name, gender, date of birth, or phone number."))

        return validated_data
    
    def save(self, request):
        user = super().save(request)
        user.is_vendor = self.validated_data.get("is_vendor", False)

        # # Disable the account for vendors temporarily
        # if user.is_vendor:
        #     user.is_active = False  # Disable account until admin approval
        user.save()

        if user.is_vendor:
            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={
                    "company_name": self.validated_data.get("company_name"),
                    "company_type": self.validated_data.get("company_type"),
                    "commercial_registration_number": self.validated_data.get("commercial_registration_number"),
                    "tax_number": self.validated_data.get("tax_number"),
                    "manager_name": self.validated_data.get("manager_name"),
                    "company_email": self.validated_data.get("company_email"),
                    "mobile_number": self.validated_data.get("mobile_number"),
                    "website": self.validated_data.get("website"),
                    "business_activity": self.validated_data.get("business_activity"),
                }
            )

            if not created:
                profile.company_name = self.validated_data.get("company_name")
                profile.company_type = self.validated_data.get("company_type")
                profile.commercial_registration_number = self.validated_data.get("commercial_registration_number")
                profile.tax_number = self.validated_data.get("tax_number")
                profile.manager_name = self.validated_data.get("manager_name")
                profile.company_email = self.validated_data.get("company_email")
                profile.mobile_number = self.validated_data.get("mobile_number")
                profile.website = self.validated_data.get("website")
                profile.business_activity = self.validated_data.get("business_activity")
                profile.save()
        else:
            # Create or update the profile for normal users
            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={
                    "first_name": self.validated_data.get("first_name"),
                    "last_name": self.validated_data.get("last_name"),
                    "gender": self.validated_data.get("gender"),
                    "date_of_birth": self.validated_data.get("date_of_birth"),
                    "phone_number": self.validated_data.get("phone_number"),
                }
            )

            if not created:
                profile.first_name = self.validated_data.get("first_name")
                profile.last_name = self.validated_data.get("last_name")
                profile.gender = self.validated_data.get("gender")
                profile.date_of_birth = self.validated_data.get("date_of_birth")
                profile.phone_number = self.validated_data.get("phone_number")
                profile.save()

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
        validated_data["is_vendor"] = user.is_vendor
        return validated_data


# class ProfileSerializer(serializers.ModelSerializer):
#     shipping_address = ShippingAddressSerializer(many=True, read_only=True, source='user.shipping_addresses')
#     billing_address = BillingAddressSerializer(many=True, read_only=True, source='user.billing_addresses')
#     avatar = serializers.ImageField(required=False, allow_null=True)

#     vendor_description = serializers.CharField(required=False, allow_blank=True)
#     store_name = serializers.CharField(required=False, allow_blank=True)
#     store_logo = serializers.ImageField(required=False, allow_null=True)

#     class Meta:
#         model = Profile
#         fields = (
#             "first_name", "last_name", "",
#             "shipping_address", "billing_address",
#             "created_at", "updated_at",
#             "vendor_description", "store_name", "store_logo",
#         )

#     def clean_text_field(self, value):
#         return value.strip() if value else None

#     def validate(self, data):
#         # Clean and validate fields without considering the language
#         data['first_name'] = self.clean_text_field(data.get('first_name'))
#         data['last_name'] = self.clean_text_field(data.get('last_name'))
#         data['bio'] = self.clean_text_field(data.get('bio'))
        
#         return data
    
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         # Set the default representation without language-specific logic
#         representation['first_name'] = instance.first_name
#         representation['last_name'] = instance.last_name
#         representation['bio'] = instance.bio

#         return representation
class ProfileSerializer(serializers.ModelSerializer):
    shipping_address = ShippingAddressSerializer(many=True, read_only=True, source='user.shipping_addresses')
    billing_address = BillingAddressSerializer(many=True, read_only=True, source='user.billing_addresses')

    # Fields common for all users
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    gender = serializers.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], required=False)
    date_of_birth = serializers.DateField(required=False)
    phone_number = serializers.CharField(max_length=15, required=False)
    
    # Fields specific to vendors
    company_name = serializers.CharField(required=False, allow_blank=True)
    company_type = serializers.CharField(required=False, allow_blank=True)
    commercial_registration_number = serializers.CharField(required=False, allow_blank=True)
    tax_number = serializers.CharField(required=False, allow_blank=True)
    manager_name = serializers.CharField(required=False, allow_blank=True)
    company_email = serializers.EmailField(required=False, allow_blank=True)
    mobile_number = serializers.CharField(required=False, allow_blank=True)
    website = serializers.URLField(required=False, allow_blank=True)
    business_activity = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Profile
        fields = (
            "first_name", "last_name", "gender", "date_of_birth", "phone_number",
            "shipping_address", "billing_address", "created_at", "updated_at",
            "company_name", "company_type", "commercial_registration_number", 
            "tax_number", "manager_name", "company_email", "mobile_number", 
            "website", "business_activity",
        )

    def validate(self, data):
        # Clean and validate fields without considering the language
        data['first_name'] = data.get('first_name', '').strip()
        data['last_name'] = data.get('last_name', '').strip()
        
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if not user:
            raise serializers.ValidationError(_("Request user is not available."))

        is_vendor = user.is_vendor if user else False
        
        if is_vendor:
            # Ensure vendor fields are provided only if the user is a vendor
            if not all(field in data and data[field] for field in [
                "company_name", "company_type", "commercial_registration_number", 
                "tax_number", "manager_name", "company_email", "mobile_number", 
                "website", "business_activity"
            ]):
                raise serializers.ValidationError(_("Vendor must provide all required vendor fields."))
            if any(field in data for field in ["gender", "date_of_birth", "phone_number"]):
                raise serializers.ValidationError(_("Vendors should not provide gender, date of birth, or phone number."))
        
        else:
            # Ensure normal user fields are provided
            if not all(field in data and data[field] for field in ["gender", "date_of_birth", "phone_number"]):
                raise serializers.ValidationError(_("Normal users must provide gender, date of birth, and phone number."))
            if any(field in data for field in [
                "company_name", "company_type", "commercial_registration_number", 
                "tax_number", "manager_name", "company_email", "mobile_number", 
                "website", "business_activity"
            ]):
                raise serializers.ValidationError(_("Normal users should not provide company-related fields."))

        return data
    
    def to_representation(self, instance):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        is_vendor = user.is_vendor if user else False

        
        representation = super().to_representation(instance)
        
        if is_vendor:
            # For vendors, include the vendor-specific fields
            representation['company_name'] = instance.company_name
            representation['company_type'] = instance.company_type
            representation['commercial_registration_number'] = instance.commercial_registration_number
            representation['tax_number'] = instance.tax_number
            representation['manager_name'] = instance.manager_name
            representation['company_email'] = instance.company_email
            representation['mobile_number'] = instance.mobile_number
            representation['website'] = instance.website
            representation['business_activity'] = instance.business_activity
        else:
            # For normal users, include the user-specific fields
            representation['first_name'] = instance.first_name
            representation['last_name'] = instance.last_name
            representation['gender'] = instance.gender
            representation['date_of_birth'] = instance.date_of_birth
            representation['phone_number'] = instance.phone_number
        
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
            "is_vendor",
            "profile",
            "shipping_address",
            "billing_address",
        )