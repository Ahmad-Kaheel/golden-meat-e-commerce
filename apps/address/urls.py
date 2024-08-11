from rest_framework.routers import DefaultRouter
from django.urls import include, path

from address.views import AddressViewSet

app_name = "addresses"

router = DefaultRouter()
router.register(r"", AddressViewSet)

urlpatterns = [
    path("address/", include(router.urls)),
]