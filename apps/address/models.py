from phonenumber_field.modelfields import PhoneNumberField

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Address(models.Model):
    
    city = models.CharField(_("City"), max_length=100)
    street_address = models.CharField(_("Street"), max_length=100)
    apartment_address = models.CharField(_("Apartment Address"), max_length=100)
    postal_code = models.CharField(_("Postal Code"), max_length=20, blank=True)

    class Meta:
        abstract = True


class ShopAddress(Address):
    shop_name = models.CharField(_("Shop Name"), max_length=255)
    owner = models.ForeignKey(User, verbose_name=_("Owner"), on_delete=models.CASCADE, related_name='shop_addresses')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "address"
        verbose_name = _("Shop Address")
        verbose_name_plural = _("Shop Addresses")
        ordering = ("-created_at",)


class UserAddress(Address):
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name='addresses')
    
    #: Whether this address should be the default for billing.
    is_default_for_billing = models.BooleanField(
        _("Default billing address?"), default=False
    )
    
    #: Whether this address is the default for shipping
    is_default_for_shipping = models.BooleanField(
        _("Default shipping address?"), default=False
    )
    
    phone_number = PhoneNumberField(
        _("Phone number"),
        blank=True,
        help_text=_("In case we need to call you about your order"),
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name=_("Instructions"),
        help_text=_("Tell us anything we should know when delivering your order."),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # `search_fields`.  This is effectively a poor man's Solr text field.
    search_text = models.TextField(
        _("Search text - used only for searching addresses"), editable=False
    )
    search_fields = [
        "address_type",
        "default",
        "city",
        "street_address",
        "apartment_address",
        "postal_code",
    ]
    
    def __str__(self):
        return f"{self.user.full_name()} - {self.city}, {self.street_address}"

    def save(self, *args, **kwargs):
        # Ensure that each user only has one default shipping address
        # and billing address
        self._ensure_defaults_integrity()
        self._update_search_text()
        super().save(*args, **kwargs)

    def _ensure_defaults_integrity(self):
        if self.is_default_for_shipping:
            self.__class__._default_manager.filter(
                user=self.user, is_default_for_shipping=True
            ).update(is_default_for_shipping=False)
        if self.is_default_for_billing:
            self.__class__._default_manager.filter(
                user=self.user, is_default_for_billing=True
            ).update(is_default_for_billing=False)    

    class Meta:
        # ShippingAddress is registered in order/models.py
        app_label = "address"
        verbose_name = _("User Address")
        verbose_name_plural = _("User Addresses")
        ordering = ("-created_at",)
    
    def clean(self):
        # Strip all whitespace
        for field in [
        "address_type",
        "default",
        "city",
        "street_address",
        "apartment_address",
        "postal_code",
    ]:
            if self.__dict__[field]:
                self.__dict__[field] = self.__dict__[field].strip()
    
    def _update_search_text(self):
        self.search_text = self.join_fields(self.search_fields, separator=" ")