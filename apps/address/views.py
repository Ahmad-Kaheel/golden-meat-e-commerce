from django.utils.translation import get_language
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from django.utils.translation import gettext as _
from address.models import ShippingAddress, BillingAddress, ShopAddress
from address.serializers import ShippingAddressSerializer, BillingAddressSerializer, ShopAddressSerializer
from customer.permissions import IsUserAddressOwner
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import(
    extend_schema, extend_schema_view, 
    OpenApiParameter, OpenApiExample
)

common_parameters = [
    OpenApiParameter(
        name='Accept-Language',
        location=OpenApiParameter.HEADER,
        description=_('Specify the language code for the response content. Supported values are "en" for English and "ar" for Arabic.'),
        required=False,
        type=str,
        examples=[
            OpenApiExample("English", value="en"),
            OpenApiExample("Arabic", value="ar")
        ]
    ),
]



@extend_schema_view(
    list=extend_schema(
        tags=['Shop Addresses'],
        summary="List all shop addresses",
        description="Retrieve a list of all shop addresses. Supports language switching via the Accept-Language header.",
        parameters=common_parameters,
    ),
    retrieve=extend_schema(
        tags=['Shop Addresses'],
        summary="Retrieve a specific shop address",
        description="Retrieve a specific shop address by its ID. Supports language switching via the Accept-Language header.",
        parameters=common_parameters,
    ),
)
class ShopAddressViewSet(ListModelMixin, 
                         RetrieveModelMixin, 
                         GenericViewSet):
    queryset = ShopAddress.objects.all()
    serializer_class = ShopAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset()



@extend_schema_view(
    list=extend_schema(
        tags=['Shipping and Billing Addresses for User'],
        summary=_('List Shipping Addresses for User'),
        description=_('List all shipping addresses associated with the authenticated user.'),
        parameters=common_parameters,
    ),
    retrieve=extend_schema(
        tags=['Shipping and Billing Addresses for User'],
        summary=_('Retrieve User Shipping Address'),
        description=_('Retrieve the shipping address associated with the authenticated user.'),
        parameters=common_parameters,
    ),
    create=extend_schema(
        tags=['Shipping and Billing Addresses for User'],
        summary=_('Create User Shipping Address'),
        description=_('Create a new shipping address for the authenticated user.'),
        parameters=common_parameters,
    ),
    update=extend_schema(
        tags=['Shipping and Billing Addresses for User'],
        summary=_('Update User Shipping Address'),
        description=_('Update the shipping address associated with the authenticated user.'),
        parameters=common_parameters,
    ),
    destroy=extend_schema(
        tags=['Shipping and Billing Addresses for User'],
        summary=_('Delete User Shipping Address'),
        description=_('Delete the shipping address associated with the authenticated user.'),
        parameters=common_parameters,
        responses={204: None},
    ),
)
class ShippingAddressViewSet(ModelViewSet):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer
    permission_classes = [IsAuthenticated, IsUserAddressOwner]

    def get_queryset(self):
        user = self.request.user
        language = get_language()
        return ShippingAddress.objects.filter(user=user)

    def get_object(self):
        user = self.request.user
        address_id = self.kwargs.get('pk')
        try:
            address = self.get_queryset().get(id=address_id)
        except ShippingAddress.DoesNotExist:
            raise PermissionDenied(_("No shipping address found for the authenticated user. Please create an address first."))
        return address

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(
    list=extend_schema(
        tags=['Shipping and Billing Addresses for User'],
        summary=_('List Billing Addresses for User'),
        description=_('List all billing addresses associated with the authenticated user.'),
        parameters=common_parameters,
    ),
    retrieve=extend_schema(
        tags=['Shipping and Billing Addresses for User'],
        summary=_('Retrieve Billing Address for User'),
        description=_('Retrieve the billing address associated with the authenticated user.'),
        parameters=common_parameters,
    ),
    create=extend_schema(
        tags=['Shipping and Billing Addresses for User'],
        summary=_('Create Billing Address for User'),
        description=_('Create a new billing address for the authenticated user.'),
        parameters=common_parameters,
    ),
    update=extend_schema(
        tags=['Shipping and Billing Addresses for User'],
        summary=_('Update Billing Address for User'),
        description=_('Update the billing address associated with the authenticated user.'),
        parameters=common_parameters,
    ),
    destroy=extend_schema(
        tags=['Shipping and Billing Addresses for User'],
        summary=_('Delete User Shipping Address'),
        description=_('Delete the shipping address associated with the authenticated user.'),
        parameters=common_parameters,
        responses={204: None},
    ),
)
class BillingAddressViewSet(ModelViewSet):
    queryset = BillingAddress.objects.all()
    serializer_class = BillingAddressSerializer
    permission_classes = [IsAuthenticated, IsUserAddressOwner]

    def get_queryset(self):
        user = self.request.user
        language = get_language()
        return BillingAddress.objects.filter(user=user)

    def get_object(self):
        user = self.request.user
        address_id = self.kwargs.get('pk')
        try:
            address = self.get_queryset().get(id=address_id)
        except BillingAddress.DoesNotExist:
            raise PermissionDenied(_("No shipping address found for the authenticated user. Please create an address first."))
        return address

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


ShippingAddressViewSet.http_method_names = ['get', 'post', 'put', 'delete']
BillingAddressViewSet.http_method_names = ['get', 'post', 'put', 'delete']
