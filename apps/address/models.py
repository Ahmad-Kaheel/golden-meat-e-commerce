import re
from modeltranslation.utils import get_translation_fields
from phonenumber_field.modelfields import PhoneNumberField

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()




class TranslatedFieldsValidationMixin:
    def clean(self):
        for field in self._meta.get_fields():
            if hasattr(self, field.name) and isinstance(field, models.CharField):
                translation_fields = get_translation_fields(field.name)
                if translation_fields:
                    filled = any(getattr(self, trans_field) for trans_field in translation_fields)
                    if not filled:
                        raise ValidationError(
                            _("Please provide the {field} in at least one language.").format(field=field.name)
                        )
        
        super().clean()



class Address(models.Model):
    """
    Abstract base class for addresses.
    """
    city = models.CharField(_("City"), max_length=100, blank=True, null=True)
    street_address = models.CharField(_("Street Address"), max_length=100, blank=True, null=True)
    apartment_address = models.CharField(_("Apartment Address"), max_length=100, blank=True, null=True)
    postal_code = models.CharField(_("Postal Code"), max_length=20, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return _("{city}, {street}").format(city=self.city, street=self.street_address)


class ShopAddress(TranslatedFieldsValidationMixin, Address):
    shop_name = models.CharField(_("Shop Name"), max_length=255)
    owner = models.ForeignKey(User, verbose_name=_("Owner"), on_delete=models.CASCADE, related_name='shop_addresses')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "address"
        verbose_name = _("Shop Address")
        verbose_name_plural = _("Shop Addresses")
        ordering = ("-created_at",)

    def __str__(self):
        return _("{shop_name} - {city}, {street}").format(
            shop_name=self.shop_name,
            city=self.city,
            street=self.street_address
        )

    def clean(self):
        for field in ['shop_name', 'city', 'street_address', 'apartment_address', 'postal_code']:
            value = getattr(self, field, None)
            if value:
                stripped_value = value.strip()
                if field == 'postal_code':
                    stripped_value = re.sub(r'[^A-Za-z0-9]', '', stripped_value).upper()
                setattr(self, field, stripped_value)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class ShippingAddress(TranslatedFieldsValidationMixin, Address):
    user = models.ForeignKey(User
                             , verbose_name=_("User"), 
                             on_delete=models.CASCADE, 
                             related_name='shipping_addresses')
    is_default_for_shipping = models.BooleanField(_("Default shipping address?"), 
                                     default=False)
    phone_number = PhoneNumberField(_("Phone Number"), 
                                    blank=True, 
                                    help_text=_("In case we need to call you about your order"))
    notes = models.TextField(_("Delivery Instructions"), 
                             blank=True, 
                             help_text=_("Tell us anything we should know when delivering your order."))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    search_text = models.TextField(_("Search text - used only for searching addresses"), 
                                   editable=False)

    search_fields = [
        "city",
        "street_address",
        "apartment_address",
        "postal_code",
    ]

    class Meta:
        app_label = "address"
        verbose_name = _("Shipping Address")
        verbose_name_plural = _("Shipping Addresses")
        ordering = ("-created_at",)
        unique_together = ('user', 'postal_code') 

    def __str__(self):
        return _("{user}: {city}, {street}").format(user=self.user.get_full_name, city=self.city, street=self.street_address)

    def clean(self):
        if self.is_default_for_shipping:
            ShippingAddress.objects.filter(user=self.user, is_default_for_shipping=True).update(is_default_for_shipping=False)
        for field in ['city', 'street_address', 'apartment_address', 'postal_code']:
            value = getattr(self, field, None)
            if value:
                setattr(self, field, value.strip())

    def save(self, *args, **kwargs):
        self.full_clean()
        self._update_search_text()
        super().save(*args, **kwargs)

    def _update_search_text(self):
        self.search_text = self.join_fields(self.search_fields, separator=" ")

    def join_fields(self, fields, separator=" "):
        return separator.join(
            str(getattr(self, field, '')) for field in fields if getattr(self, field)
        )


class BillingAddress(TranslatedFieldsValidationMixin, Address):
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name='billing_addresses')
    is_default_for_billing = models.BooleanField(_("Default billing address?"), default=False)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        app_label = "address"
        verbose_name = _("Billing Address")
        verbose_name_plural = _("Billing Addresses")
        ordering = ("-created_at",)
        unique_together = ('user', 'postal_code') 

    def __str__(self):
        return _("{user}: {city}, {street}").format(user=self.user.get_full_name, city=self.city, street=self.street_address)

    def clean(self):
        if self.is_default_for_billing:
            BillingAddress.objects.filter(user=self.user, is_default_for_billing=True).update(is_default_for_billing=False)
        for field in ['city', 'street_address', 'apartment_address', 'postal_code']:
            value = getattr(self, field, None)
            if value:
                setattr(self, field, value.strip())

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)