from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.exceptions import PermissionDenied
from django.utils.translation import gettext as _

from address.models import UserAddress
from address.serializers import AddressSerializer
from customer.permissions import IsUserAddressOwner
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse



@extend_schema_view(
    get=extend_schema(
        tags=['User Address'],
        summary='Retrieve User Address',
        description='Retrieve the address associated with the authenticated user.'
    ),
    put=extend_schema(
        tags=['User Address'],
        summary='Update User Address',
        description='Update the address associated with the authenticated user.'
    ),
    patch=extend_schema(
        tags=['User Address'],
        summary='Partially Update User Address',
        description='Partially update the address associated with the authenticated user.'
    ),
    post=extend_schema(
        tags=['User Address'],
        summary='Create User Address',
        description='Create a new address for the authenticated user.'
    ),
)
class UserAddressAPIView(RetrieveUpdateAPIView, CreateAPIView):
    """
    Get, Update, and Create user address
    """

    queryset = UserAddress.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated, IsUserAddressOwner]

    def get_object(self):
        user = self.request.user
        try:
            address = self.queryset.get(user=user)
        except UserAddress.DoesNotExist:
            raise PermissionDenied(_("No address found for the authenticated user. Please create an address first."))
        return address

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)