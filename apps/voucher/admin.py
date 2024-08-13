from django.contrib import admin
from voucher.models import Coupon, UserCoupon

@admin.register(Coupon)
class CouponsAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'discount']
    list_display_links = ['id']
    list_editable = ['product']
    search_fields = ['id', 'product', 'coupon', 'discount']
    exclude = ['coupon']


admin.site.register(UserCoupon)
