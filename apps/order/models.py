import random
from datetime import date
from django.core.exceptions import ValidationError

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from catalogue.models import Product
from address.models import ShippingAddress, BillingAddress
from voucher.models import UserCoupon, Coupon
from basket.models import Basket


User = get_user_model()


class Order(models.Model):
    ORDER_STATUSES = (
        (1, _('New')),
        (2, _('Processing')),
        (3, _('Ready to ship')),
        (4, _('Shipped')),
        (5, _('Delivered')),
        (6, _('Canceled'))
    )
    PAYMENT_METHODS = (
        (1, _('By cash')),
        (2, _('By card'))
    )
    DELIVERY_METHODS = (
        (1, _('Courier')),
        (2, _('To the post office'))
    )
    
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name=_('User'),
                             related_name='orders',
                             blank=True,
                             null=True)

    basket = models.OneToOneField(Basket,
                                  on_delete=models.CASCADE,
                                  verbose_name=_('Basket'),
                                  related_name='order',
                                  blank=True,
                                  null=True)
    
    order_id = models.CharField(max_length=7, blank=True, null=True)
    order_status = models.IntegerField(verbose_name=_('Order status'),
                                       choices=ORDER_STATUSES,
                                       default=1)
    coupon = models.ForeignKey(UserCoupon,
                               on_delete=models.SET_NULL,
                               verbose_name=_('Coupon'),
                               blank=True,
                               null=True)
    total_amount = models.IntegerField(default=0,
                                       verbose_name=_('Total amount of order'))
    shipping_info = models.ForeignKey(ShippingAddress,
                                      on_delete=models.SET_NULL,
                                      verbose_name=_('User shipping info'),
                                      blank=True,
                                      null=True,
                                      related_name='shipping_orders')
    billing_info = models.ForeignKey(BillingAddress,
                                      on_delete=models.SET_NULL,
                                      verbose_name=_('User billing info'),
                                      blank=True,
                                      null=True,
                                      related_name='billing_orders')
    payment_method = models.IntegerField(default=1,
                                         choices=PAYMENT_METHODS,
                                         verbose_name=_('Payment method'))
    delivery_method = models.IntegerField(default=2,
                                          choices=DELIVERY_METHODS,
                                          verbose_name=_('Delivery method'))
    comment = models.TextField(max_length=1000,
                               verbose_name=_('Comment'),
                               blank=True,
                               null=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    
    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['total_amount']

    def __str__(self):
        return _('Order #: %(id)s, order_id: %(order_id)s') % {
            'id': self.id,
            'order_id': self.order_id or 'N/A'
        }
    
    def clean(self):
        if self.coupon and self.total_amount < self.coupon.discount:
            raise ValidationError(_('Coupon discount cannot exceed total amount.'))

        if self.coupon and self.coupon.valid_to and self.coupon.valid_to < date.today():
            raise ValidationError(_('The coupon has expired.'))

        if self.coupon and not self.coupon.is_active:
            raise ValidationError(_('The coupon is not active.'))

        super().clean()


class OrderItems(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              verbose_name=_('Order'),
                              related_name='items')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                verbose_name=_('Product'))
    quantity = models.IntegerField(default=0,
                                   verbose_name=_('Quantity'))
    total_price = models.IntegerField(default=0,
                                      verbose_name=_('Total price'))

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('Items in order')
        ordering = ['total_price']

    def __str__(self):
        return _('Item: %(product_name)s, Order: %(order_id)s') % {
            'product_name': self.product.title,
            'order_id': self.order.order_id or self.order.id
        }
    
    def clean(self):
        if self.quantity <= 0:
            raise ValidationError(_('Quantity must be greater than zero.'))

        if self.product and self.quantity > self.product.stock:
            raise ValidationError(_('Quantity exceeds available stock.'))

        super().clean()
    
    def get_coupon(self, coupon) -> bool:
        coupon_drop_chance = coupon.drop_chance
        random_percent = random.uniform(0, 1)
        if random_percent <= coupon_drop_chance:
            return True
        return False

    def check_coupon_eligibility(self, user):
        coupons = Coupon.objects.filter(product=self.product)
        
        for coupon in coupons:
            user_purchases = OrderItems.objects.filter(order__user=user, product=self.product).aggregate(
                total_quantity=models.Sum('quantity')
            )['total_quantity'] or 0

            total_quantity = user_purchases + self.quantity

            if total_quantity >= coupon.quantity_threshold:
                if self.get_coupon(coupon):
                    return coupon
        
        return None