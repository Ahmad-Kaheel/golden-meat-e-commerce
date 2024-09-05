from django.contrib import admin
from django import forms
from django.utils.translation import gettext_lazy as _

from basket.models import Basket, BasketItems


class BasketItemsInline(admin.TabularInline):
    model = BasketItems
    extra = 1
    readonly_fields = ('total_price',)
    can_delete = True
    fields = ('product', 'quantity', 'total_price')
    widgets = {
        'product': forms.Select(attrs={'size': '10'}),
        'quantity': forms.NumberInput(attrs={'size': '10'}),
        'total_price': forms.TextInput(attrs={'readonly': 'readonly'}),
    }

class BasketAdmin(admin.ModelAdmin):
    list_display = ('get_user_full_name', 'created_at', 'total_quantity', 'total_amount')
    list_filter = ('created_at',)
    search_fields = ('get_user_full_name', 'user__email')
    inlines = [BasketItemsInline]
    readonly_fields = ('total_amount',)
    
    def total_amount(self, obj):
        return obj.total_amount
    total_amount.admin_order_field = 'total_amount'
    total_amount.short_description = _('Total amount')

    def total_quantity(self, obj):
        return obj.total_quantity
    total_amount.admin_order_field = 'total_quantity'
    total_amount.short_description = _('Total Quantity')


    def get_user_full_name(self, obj):
        return obj.user.get_full_name
    get_user_full_name.short_description = _('User Full Name')

class BasketItemsAdmin(admin.ModelAdmin):
    list_display = ('basket', 'product', 'quantity', 'total_price')
    list_filter = ('basket', 'product')
    search_fields = ('basket__user__get_full_name', 'product__title')
    readonly_fields = ('total_price',)

admin.site.register(Basket, BasketAdmin)
admin.site.register(BasketItems, BasketItemsAdmin)


def get_user_full_name(self, obj):
        return obj.user.get_full_name
get_user_full_name.short_description = _('User Full Name')