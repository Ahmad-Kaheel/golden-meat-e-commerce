from decimal import Decimal
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view

from rest_framework import permissions, viewsets
from rest_framework import generics


from catalogue.models import Product, Category
from catalogue.serializers import (
    ProductCategoryReadSerializer,
    ProductReadSerializer,
)


@extend_schema_view(
    list=extend_schema(tags=['Category and Product']),
    retrieve=extend_schema(tags=['Category and Product']),
)
class ProductCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and Retrieve product categories
    """

    queryset = Category.objects.browsable()
    serializer_class = ProductCategoryReadSerializer
    permission_classes = (permissions.AllowAny,)


@extend_schema_view(
    list=extend_schema(tags=['Category and Product']),
    retrieve=extend_schema(tags=['Category and Product']),
)
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and Retrieve product
    """

    queryset = Product.objects.browsable()
    serializer_class = ProductReadSerializer
    permission_classes = (permissions.AllowAny,)

    # def get_serializer_class(self):
    #     if self.action in ("create", "update", "partial_update", "destroy"):
    #         return ProductWriteSerializer
    #     return ProductReadSerializer

    # def get_permissions(self):
    #     if self.action in ("create",):
    #         self.permission_classes = (permissions.IsAdminUser,)
    #     elif self.action in ("update", "partial_update", "destroy"):
    #         self.permission_classes = (permissions.IsAdminUser,)
    #     else:
    #         self.permission_classes = (permissions.AllowAny,)

    #     return super().get_permissions()

@extend_schema(
    tags=['Product Filter'],
    parameters=[
        OpenApiParameter(name='country_id', description='Filter by country', required=False, type=str),
        OpenApiParameter(name='min_price', description='Minimum price', required=False, type=float),
        OpenApiParameter(name='max_price', description='Maximum price', required=False, type=float),
        OpenApiParameter(name='category_id', description='Filter by category', required=False, type=str),
        OpenApiParameter(name='recommended_for', description='Filter by recommended products', required=False, type=str),
        OpenApiParameter(name='include_non_public', description='Include non-public products', required=False, type=bool),
        OpenApiParameter(name='out_of_stock', description='Include out-of-stock products', required=False, type=bool),
        OpenApiParameter(name='limit', description='Number of results to return per page', required=False, type=int),
        OpenApiParameter(name='offset', description='The initial index from which to return the results', required=False, type=int),
    ],
    responses=ProductReadSerializer(many=True),
)
class ProductFilterAPIView(generics.ListAPIView):
    serializer_class = ProductReadSerializer
    
    
    def get_queryset(self):
        country_id = self.request.query_params.get('country_id')
        min_price = self.request.query_params.get('min_price')
        print("min_price min_price min_price ", min_price, type(min_price))
        max_price = self.request.query_params.get('max_price')
        print("max_price max_price max_price ", max_price)
        category_id = self.request.query_params.get('category_id')
        recommended_for = self.request.query_params.get('recommended_for')
        
        return Product.objects.browsable().filter_products(
            country_id,
            min_price,
            max_price,
            category_id,
            recommended_for,
        )

