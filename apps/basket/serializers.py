from rest_framework import serializers

from basket.models import Basket, BasketItems
from customer.serializers import UserSerializer


class BasketSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()

    class Meta:
        model = Basket
        fields = ('user', 'user_email')

    def get_user_email(self, obj):
        user = obj.user
        user_serializer = UserSerializer(instance=user)
        return user_serializer.data['email']


class BasketItemsSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = BasketItems
        fields = ('product', 'product_name', 'quantity', 'total_price')

    def get_product_name(self, obj):
        return obj.product.title