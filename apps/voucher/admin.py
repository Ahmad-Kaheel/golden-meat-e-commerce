from django.contrib import admin
from voucher.models import Coupon, UserCoupon

class CouponAdmin(admin.ModelAdmin):
    list_display = (
        'coupon',
        'product',
        'discount',
        'drop_chance',
        'quantity_threshold'
    )
    list_filter = (
        'product',
        'discount',
        'drop_chance',
    )
    search_fields = (
        'coupon',
        'product__title',
    )
    readonly_fields = ('coupon',)
    ordering = ('-discount',)

class UserCouponAdmin(admin.ModelAdmin):
    list_display = (
        'coupon',
        'user',
        'started_at',
        'valid_to',
        'is_active'
    )
    list_filter = (
        'is_active',
        'started_at',
        'valid_to',
    )
    search_fields = (
        'user__email',
        'coupon__product__title',
        'coupon__coupon',
    )
    readonly_fields = ('started_at', 'valid_to')
    ordering = ('-started_at',)

admin.site.register(Coupon, CouponAdmin)
admin.site.register(UserCoupon, UserCouponAdmin)
