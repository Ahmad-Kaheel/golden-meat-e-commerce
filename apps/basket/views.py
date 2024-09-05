from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import(
    extend_schema, extend_schema_view, 
    OpenApiParameter, OpenApiExample
) 

from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _

from basket.utils import BasketMixin, BasketOperationTypes
from catalogue.models import Product


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
    get=extend_schema(
        tags=['Basket operations'],
        summary=_("Retrieve Basket Data"),
        parameters=common_parameters
    ),
)
class BasketAPIView(BasketMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        data = self.get_basket_data(self.request)
        if len(data['items']) > 0:
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response({'basket': _('You don’t have items in your basket!')}, status=status.HTTP_200_OK)


@extend_schema_view(
    post=extend_schema(
        tags=['Basket operations'],
        summary=_("Handle Basket Operations"),
        parameters=common_parameters
    ),
)
class OperationBasketAPIView(BasketMixin, APIView):
    """
    Base class for basket operations, handles POST requests.
    """
    def post(self, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs['product_id'])
        if product.quantity != 0:
            data = self.basket_operation(self.request, product)
            return Response(data=data)
        else:
            return Response({'not available': _('This product is currently out of stock.')}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Basket operations'],
    summary=_("Add to Basket"),
    parameters=common_parameters
)
class AddToBasketAPIView(OperationBasketAPIView):
    operation_type = BasketOperationTypes.basket_add


@extend_schema(
    tags=['Basket operations'],
    summary=_("Increase Quantity of Basket Item"),
    parameters=common_parameters
)
class BasketItemAddQuantityAPIView(OperationBasketAPIView):
    operation_type = BasketOperationTypes.item_add_quantity


@extend_schema(
    tags=['Basket operations'],
    summary=_("Decrease Quantity of Basket Item"),
    parameters=common_parameters
)
class BasketItemMinusQuantityAPIView(OperationBasketAPIView):
    operation_type = BasketOperationTypes.item_minus_quantity


@extend_schema_view(
    get=extend_schema(
        tags=['Basket operations'],
        summary=_("Retrieve Basket"),
        parameters=common_parameters
    ),
    post=extend_schema(
        tags=['Basket operations'],
        summary=_("Clear Basket"),
        parameters=common_parameters
    )
)
class BasketClearAPIView(OperationBasketAPIView):
    operation_type = BasketOperationTypes.basket_clear

    def get(self, *args, **kwargs):
        data = self.get_basket_data(self.request)
        return Response(data=data)

    def post(self, *args, **kwargs):
        data = self.basket_operation(self.request)
        return Response(data=data)
