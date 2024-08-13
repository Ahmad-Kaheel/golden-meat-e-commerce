from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view

from rest_framework import permissions, viewsets
from rest_framework import generics


from catalogue.models import Product, Category, Review
from catalogue.serializers import (
    ProductCategoryReadSerializer,
    ProductReadSerializer,
    ReviewSerializer,
)
from customer.permissions import IsUserAddressOwner as IsReviewOwnerOrAdmin


@extend_schema_view(
    list=extend_schema(
        tags=['Category and Product'],
        summary="List product categories",
        description="Retrieve a list of all product categories that are available."
    ),
    retrieve=extend_schema(
        tags=['Category and Product'],
        summary="Retrieve a product category",
        description="Retrieve a specific product category by ID."
    ),
)
class ProductCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and Retrieve product categories
    """

    queryset = Category.objects.browsable()
    serializer_class = ProductCategoryReadSerializer
    permission_classes = (permissions.AllowAny,)


@extend_schema_view(
    list=extend_schema(
        tags=['Category and Product'],
        summary="List products",
        description="Retrieve a list of all products that are available."
    ),
    retrieve=extend_schema(
        tags=['Category and Product'],
        summary="Retrieve a product",
        description="Retrieve a specific product by ID."
    ),
)
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and Retrieve product
    """

    queryset = Product.objects.browsable()
    serializer_class = ProductReadSerializer
    permission_classes = (permissions.AllowAny,)


@extend_schema(
    tags=['Product Filter'],
    summary="Filter products",
    description="Filter products based on various criteria such as country, price range, category, and more.",
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
        # print("min_price min_price min_price ", min_price, type(min_price))
        max_price = self.request.query_params.get('max_price')
        # print("max_price max_price max_price ", max_price)
        category_id = self.request.query_params.get('category_id')
        recommended_for = self.request.query_params.get('recommended_for')
        
        return Product.objects.browsable().filter_products(
            country_id,
            min_price,
            max_price,
            category_id,
            recommended_for,
        )



@extend_schema_view(
    list=extend_schema(
        summary="List all reviews",
        description="Retrieve a list of all reviews.",
        tags=["Reviews"]
    ),
    create=extend_schema(
        summary="Create a review",
        description="Create a new review. Only authenticated users can create reviews.",
        tags=["Reviews"]
    ),
    retrieve=extend_schema(
        summary="Retrieve a review",
        description="Retrieve a specific review by ID.",
        tags=["Reviews"]
    ),
    update=extend_schema(
        summary="Update a review",
        description="Update a specific review. Only admins or the owner can update reviews.",
        tags=["Reviews"]
    ),
    partial_update=extend_schema(
        summary="Partially update a review",
        description="Partially update a specific review. Only admins or the owner can update reviews.",
        tags=["Reviews"]
    ),
    destroy=extend_schema(
        summary="Delete a review",
        description="Delete a specific review. Only admins or the owner can delete reviews.",
        tags=["Reviews"]
    )
)
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsReviewOwnerOrAdmin,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)