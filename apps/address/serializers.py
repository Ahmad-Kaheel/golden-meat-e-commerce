import re
from rest_framework import serializers
from address.models import ShopAddress, ShippingAddress, BillingAddress


class ShopAddressSerializer(serializers.ModelSerializer):
    shop_name = serializers.CharField()

    class Meta:
        model = ShopAddress
        fields = ['id', 'shop_name', 'city', 'street_address', 
                  'apartment_address', 'postal_code', 'created_at']


class ShippingAddressSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:
        model = ShippingAddress
        fields = [
            'id', 'user', 'city', 'street_address', 'apartment_address',
            'postal_code', 'is_default_for_shipping', 'phone_number',
            'notes', 'created_at',
        ]

    def clean_text_field(self, value):
        return value.strip() if value else None

    def clean_postal_code(self, value):
        return re.sub(r'[^A-Za-z0-9]', '', value).upper() if value else None

    def validate(self, data):
        data['city'] = self.clean_text_field(data.get('city'))
        data['street_address'] = self.clean_text_field(data.get('street_address'))
        data['apartment_address'] = self.clean_text_field(data.get('apartment_address'))
        data['notes'] = self.clean_text_field(data.get('notes'))
        data['postal_code'] = self.clean_postal_code(data.get('postal_code'))
        return data



class BillingAddressSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:
        model = BillingAddress
        fields = [
            'id', 'user', 'city', 'street_address', 'apartment_address',
            'postal_code', 'is_default_for_billing', 'created_at',
        ]

    def clean_text_field(self, value):
        return value.strip() if value else None

    def clean_postal_code(self, value):
        return re.sub(r'[^A-Za-z0-9]', '', value).upper() if value else None

    def validate(self, data):
        data['city'] = self.clean_text_field(data.get('city'))
        data['street_address'] = self.clean_text_field(data.get('street_address'))
        data['apartment_address'] = self.clean_text_field(data.get('apartment_address'))
        data['postal_code'] = self.clean_postal_code(data.get('postal_code'))
        return data