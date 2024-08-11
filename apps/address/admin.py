from django.contrib import admin

from address.models import UserAddress, ShopAddress

admin.site.register(UserAddress)
admin.site.register(ShopAddress)