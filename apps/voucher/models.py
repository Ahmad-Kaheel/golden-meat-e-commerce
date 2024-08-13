import binascii
import os

from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _

from catalogue.models import Product
from voucher.services import generate_end_date
from django.contrib.auth import get_user_model

User = get_user_model()


class Coupon(models.Model):
    coupon = models.CharField(
        max_length=16,
        verbose_name=_("Coupon"),
        blank=True,
        null=True
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("Product"),
        related_name='coupon'
    )
    discount = models.PositiveSmallIntegerField(
        default=1,
        verbose_name=_("Discount")
    )
    drop_chance = models.PositiveSmallIntegerField(
        default=1,
        verbose_name=_("Chance to drop")
    )

    class Meta:
        verbose_name = _("coupon")
        verbose_name_plural = _("Coupons")
        ordering = ['discount']

    def __str__(self):
        return _('Coupon for: %(product_title)s') % {'product_title': self.product.title}
    
    @staticmethod
    def generate_coupon():
        return binascii.hexlify(os.urandom(8)).decode()
    
    def save(self, *args, **kwargs):
        if self._state.adding and (not self.coupon or Coupon.objects.filter(coupon=self.coupon).exists()):
            self.coupon = self.generate_coupon().upper()
        super().save(*args, **kwargs)



class UserCoupon(models.Model):
    coupon = models.ForeignKey(Coupon,
                               on_delete=models.CASCADE,
                               verbose_name=_('Coupon'))
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name=_('User'),
                             related_name='coupons')
    started_at = models.DateField(auto_now_add=True,
                                  verbose_name=_('Coupon start date'))
    valid_to = models.DateField(verbose_name=_('Coupon valid to'),
                                blank=True,
                                null=True)
    is_active = models.BooleanField(default=True,
                                    verbose_name=_('Is active'))

    class Meta:
        verbose_name = _('user coupon')
        verbose_name_plural = _("Users' coupons")

    def __str__(self):
        return _('Coupon for product: %(product_name)s. Discount: %(discount)s%%') % {
            'product_name': self.product.title,
            'discount': self.discount
        }

    def save(self, *args, **kwargs):
        if self.started_at is None:
            self.started_at = timezone.now()
        self.valid_to = generate_end_date(self.started_at)
        super().save(*args, **kwargs)