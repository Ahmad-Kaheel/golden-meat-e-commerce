# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from address.views import ShippingAddressViewSet, BillingAddressViewSet, ShopAddressViewSet

app_name = "addresse"

router = DefaultRouter()
router.register(r'shop-addresses', ShopAddressViewSet, basename='shop-address')
router.register(r'shipping-address', ShippingAddressViewSet, basename='shipping-address')
router.register(r'billing-address', BillingAddressViewSet, basename='billing-address')

urlpatterns = [
    path('', include(router.urls)),
]
