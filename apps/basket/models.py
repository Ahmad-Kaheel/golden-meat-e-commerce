from django.db import models
from django.utils.translation import gettext_lazy as _

from catalogue.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()


class Basket(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                verbose_name=_('User'),
                                blank=True,
                                null=True,
                                related_name='basket')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Created at'))

    class Meta:
        verbose_name = _('Basket')
        verbose_name_plural = _('Baskets')

    def __str__(self):
        return _('Basket of %(username)s') % {'username': self.user.get_full_name}

    def __len__(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_amount(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def total_quantity(self):
        return self.__len__()
    
class BasketItems(models.Model):
    basket = models.ForeignKey(Basket,
                               on_delete=models.CASCADE,
                               verbose_name=_('Basket'),
                               related_name='items')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                verbose_name=_('Product'))
    quantity = models.IntegerField(default=0,
                                   verbose_name=_('Item quantity'))
    total_price = models.IntegerField(default=0,
                                      verbose_name=_('Total price of item'))

    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = _('Basket items')

    def __str__(self):
        return _('Basket item %(product_name)s') % {'product_name': self.product.title}

    def save(self, *args, **kwargs):
        if self.product.discount:
            self.total_price = self.product.price_with_discount * self.quantity
        else:
            self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)
