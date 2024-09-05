from django.db import models
from django.utils.translation import gettext_lazy as _

from order.models import Order
from address.models import ShippingAddress, BillingAddress


class PaymentInfo(models.Model):
    order = models.OneToOneField(Order,
                                 on_delete=models.CASCADE,
                                 verbose_name=_('Order'),
                                 related_name='payment_info',
                                 help_text=_('The order associated with this payment.'))
    billing_info = models.ForeignKey(BillingAddress,
                                      on_delete=models.SET_NULL,
                                      verbose_name=_('User billing info'),
                                      blank=True, related_name='billing_info', 
                                      null=True,
                                      help_text=_('The billing information for the user making this payment.'))
    shipping_info = models.ForeignKey(BillingAddress,
                                      on_delete=models.SET_NULL,
                                      verbose_name=_('User shipping info'),
                                      blank=True, related_name='shipping_info', 
                                      null=True,
                                      help_text=_('The shipping information for the user making this payment.'))
    payment_method = models.IntegerField(choices=Order.PAYMENT_METHODS,
                                         verbose_name=_('Payment method'),
                                         help_text=_('The method used for payment, such as credit card or PayPal.'))
    payment_amount = models.IntegerField(default=0,
                                         verbose_name=_('Payment amount'),
                                         help_text=_('The total amount paid for the order.'))
    payment_date = models.DateTimeField(verbose_name=_('Payment date'),
                                        blank=True,
                                        null=True,
                                        help_text=_('The date and time when the payment was made.'))
    is_paid = models.BooleanField(default=False,
                                  verbose_name=_('Order is paid'),
                                  help_text=_('Indicates whether the order has been fully paid.'))
    bonus_taken = models.BooleanField(default=False,
                                      verbose_name=_('Bonus taken'),
                                      help_text=_('Indicates whether any bonus or discount was applied to the payment.'))

    class Meta:
        verbose_name = _('payment info')
        verbose_name_plural = _('Payment infos')

    def __str__(self):
        return _('Payment info order id: %(order_id)s') % {'order_id': self.order_id}
