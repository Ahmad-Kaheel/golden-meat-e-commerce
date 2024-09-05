from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from django.utils.translation import gettext_lazy as _

from address.models import ShippingAddress, BillingAddress, ShopAddress

@register(ShippingAddress)
class ShippingAddressTranslationOptions(TranslationOptions):
    fields = ('city', 'street_address', 'apartment_address', 'notes')

@register(BillingAddress)
class BillingAddressTranslationOptions(TranslationOptions):
    fields = ('city', 'street_address', 'apartment_address')

@register(ShopAddress)
class ShopAddressTranslationOptions(TranslationOptions):
    fields = ('shop_name', 'city', 'street_address', 'apartment_address')