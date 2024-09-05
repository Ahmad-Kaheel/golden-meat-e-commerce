from django.contrib import admin
from django import forms
from address.models import ShippingAddress, BillingAddress, ShopAddress


class AddressAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            'city': forms.TextInput(attrs={'size': '40'}),
            'street_address': forms.TextInput(attrs={'size': '40'}),
            'apartment_address': forms.TextInput(attrs={'size': '40'}),
            'postal_code': forms.TextInput(attrs={'size': '20'}),
            'phone_number': forms.TextInput(attrs={'size': '20'}),
        }


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    form = AddressAdminForm
    list_display = ('user', 'city', 'street_address', 'postal_code', 'is_default_for_shipping')
    list_filter = ('is_default_for_shipping', 'created_at')
    search_fields = ('city', 'street_address', 'apartment_address', 'postal_code')
    ordering = ('-created_at',)


@admin.register(BillingAddress)
class BillingAddressAdmin(admin.ModelAdmin):
    form = AddressAdminForm
    list_display = ('user', 'city', 'street_address', 'postal_code', 'is_default_for_billing')
    list_filter = ('is_default_for_billing', 'created_at')
    search_fields = ('city', 'street_address', 'apartment_address', 'postal_code')
    ordering = ('-created_at',)


@admin.register(ShopAddress)
class ShopAddressAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'city', 'street_address', 'postal_code', 'owner', 'created_at')
    list_filter = ('city', 'created_at')
    search_fields = ('shop_name', 'city', 'street_address', 'postal_code')
    ordering = ('-created_at',)


