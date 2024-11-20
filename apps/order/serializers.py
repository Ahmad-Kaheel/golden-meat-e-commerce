from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

from order.utils import OrderMixin
from order.models import Order, OrderItems, DeliverySettings
from address.serializers import ShippingAddressSerializer, BillingAddressSerializer
from address.models import ShippingAddress, BillingAddress
from voucher.models import UserCoupon



class OrderItemsSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title')
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = OrderItems
        fields = ['product_title', 'quantity', 'product_price', 'total_price']


class OrderSerializer(OrderMixin, serializers.ModelSerializer):
    shipping_info = serializers.PrimaryKeyRelatedField(queryset=ShippingAddress.objects.all())
    billing_info = serializers.PrimaryKeyRelatedField(queryset=BillingAddress.objects.all())
    order_items = OrderItemsSerializer(many=True, source='items', read_only=True)
    coupon = serializers.CharField(write_only=True, required=False, allow_blank=True)
    payment_method_display = serializers.SerializerMethodField()
    delivery_method_display = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'shipping_info', 'billing_info', 'payment_method', 'delivery_method', 
                  'payment_method_display', 'delivery_method_display', 'coupon', 'comment', 
                  'total_amount', 'order_items', 'delivery_cost', 'free_delivery')
        read_only_fields = ['total_amount']

    def get_payment_method_display(self, obj):
        return dict(Order.PAYMENT_METHODS).get(obj.payment_method, "")

    def get_delivery_method_display(self, obj):
        return dict(Order.DELIVERY_METHODS).get(obj.delivery_method, "")

    def create(self, validated_data):
        request = self.context.get('request')

        shipping_info = validated_data.pop('shipping_info')
        billing_info = validated_data.pop('billing_info')
        coupon_code = validated_data.pop('coupon', None)

        order = Order(
            shipping_info=shipping_info,
            billing_info=billing_info,
            **validated_data
        )

        if request.user.is_authenticated:
            order.user = request.user

            if coupon_code:
                try:
                    user_coupon = UserCoupon.objects.get(
                        coupon__coupon=coupon_code,
                        user=request.user,
                        is_active=True
                    )
                    order.coupon = user_coupon
                except UserCoupon.DoesNotExist:
                    raise serializers.ValidationError({"coupon": _("Invalid coupon code or coupon not available.")})

        order.save()
        return order

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        ret['shipping_info'] = ShippingAddressSerializer(instance.shipping_info).data
        ret['billing_info'] = BillingAddressSerializer(instance.billing_info).data
        if instance.coupon:
            ret['coupon'] = instance.coupon.coupon.coupon

        return ret



class DeliverySettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliverySettings
        fields = ['fixed_cost', 'free_delivery_threshold']
