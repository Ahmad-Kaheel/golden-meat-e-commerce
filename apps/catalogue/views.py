from drf_spectacular.utils import(
    extend_schema, extend_schema_view, 
    OpenApiParameter, OpenApiExample
) 
from rest_framework import permissions, viewsets
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from catalogue.models import Product, Category, Review
from catalogue.serializers import (
    ProductCategoryReadSerializer,
    ProductReadSerializer,
    ReviewSerializer,
)
from customer.permissions import IsUserAddressOwner as IsReviewOwnerOrAdmin


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
        tags=['Category and Product'],
        summary="List product categories",
        description="Retrieve a list of all product categories that are available.",
        parameters=common_parameters,
    ),
    retrieve=extend_schema(
        tags=['Category and Product'],
        summary="Retrieve a product category",
        description="Retrieve a specific product category by ID.",
        parameters=common_parameters,
    ),
)
class ProductCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and Retrieve product categories
    """

    queryset = Category.objects.browsable()
    serializer_class = ProductCategoryReadSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        language = get_language()

        if language == 'ar':
            return Category.objects.browsable().filter(name_ar__isnull=False)
        else:
            return Category.objects.browsable().filter(name_en__isnull=False)


@extend_schema_view(
    list=extend_schema(
        tags=['Category and Product'],
        summary=_("List products"),
        description=_("Retrieve a list of all products that are available."),
        parameters=common_parameters,
    ),
    retrieve=extend_schema(
        tags=['Category and Product'],
        summary=_("Retrieve a product"),
        description=_("Retrieve a specific product by ID."),
        parameters=common_parameters,
    ),
)
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and Retrieve product
    """

    queryset = Product.objects.browsable().prefetch_related('categories', 'source_country', 'specifications', 'recommended_products', 'review_set')
    serializer_class = ProductReadSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        language = get_language()

        queryset = super().get_queryset()

        if language == 'ar':
            return queryset.filter(title_ar__isnull=False)
        else:
            return queryset.filter(title_en__isnull=False)



@extend_schema(
    tags=['Product Filter'],
    summary=_("Filter products"),
    description=_("Filter products based on various criteria such as country, price range, category, and more."),
    parameters=[
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
        OpenApiParameter(name='country_id', description=_('Filter by country'), required=False, type=str),
        OpenApiParameter(name='min_price', description=_('Minimum price'), required=False, type=float),
        OpenApiParameter(name='max_price', description=_('Maximum price'), required=False, type=float),
        OpenApiParameter(name='category_id', description=_('Filter by category'), required=False, type=str),
        OpenApiParameter(name='recommended_for', description=_('Filter by recommended products'), required=False, type=str),
        OpenApiParameter(name='limit', description=_('Number of results to return per page'), required=False, type=int),
        OpenApiParameter(name='offset', description=_('The initial index from which to return the results'), required=False, type=int),
    ],
    responses=ProductReadSerializer(many=True),
)
class ProductFilterAPIView(generics.ListAPIView):
    serializer_class = ProductReadSerializer

    def get_queryset(self):
        country_id = self.request.query_params.get('country_id')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        category_id = self.request.query_params.get('category_id')
        recommended_for = self.request.query_params.get('recommended_for')

        queryset = Product.objects.browsable().filter_products(
            country_id,
            min_price,
            max_price,
            category_id,
            recommended_for,
        )

        language = get_language()

        if language == 'ar':
            return queryset.filter(title_ar__isnull=False)
        else:
            return queryset.filter(title_en__isnull=False)





@extend_schema_view(
    list=extend_schema(
        summary=_("List all reviews"),
        description=_("Retrieve a list of all reviews."),
        tags=["Reviews"],
    ),
    create=extend_schema(
        summary=_("Create a review"),
        description=_("Create a new review. Only authenticated users can create reviews."),
        tags=["Reviews"],
    ),
    retrieve=extend_schema(
        summary=_("Retrieve a review"),
        description=_("Retrieve a specific review by ID."),
        tags=["Reviews"],
    ),
    update=extend_schema(
        summary=_("Update a review"),
        description=_("Update a specific review. Only admins or the owner can update reviews."),
        tags=["Reviews"],
    ),
    partial_update=extend_schema(
        summary=_("Partially update a review"),
        description=_("Partially update a specific review. Only admins or the owner can update reviews."),
        tags=["Reviews"],
    ),
    destroy=extend_schema(
        summary=_("Delete a review"),
        description=_("Delete a specific review. Only admins or the owner can delete reviews."),
        tags=["Reviews"],
    )
)
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.action == 'list':
            return Review.objects.filter(parent__isnull=True)
        return Review.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        parent = serializer.validated_data.get('parent', None)

        if parent and not user.is_staff:
            raise PermissionDenied(_("You are not allowed to reply to other users' reviews."))

        serializer.save(user=user)

    def perform_update(self, serializer):
        user = self.request.user
        instance = self.get_object()

        if instance.user != user and not user.is_staff:
            raise PermissionDenied(_("You do not have permission to edit this review."))

        if instance.parent and not user.is_staff:
            serializer.validated_data.pop('rating', None)
        
        serializer.save()
