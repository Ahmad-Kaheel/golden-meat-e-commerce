from rest_framework import permissions, status
from rest_framework.viewsets import ReadOnlyModelViewSet

from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model

from address.models import UserAddress
from customer.permissions import IsUserAddressOwner
from address.serializers import AddressReadOnlySerializer

class AddressViewSet(ReadOnlyModelViewSet):
    """
    List and Retrieve user addresses
    """

    queryset = UserAddress.objects.all()
    serializer_class = AddressReadOnlySerializer
    permission_classes = (IsUserAddressOwner,)

    def get_queryset(self):
        res = super().get_queryset()
        user = self.request.user
        return res.filter(user=user)