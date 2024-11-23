from haystack.query import SearchQuerySet
from drf_spectacular.utils import(
    extend_schema, extend_schema_view, 
    OpenApiParameter, OpenApiExample
) 
from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from catalogue.models import Product, Category, Review, Country
from catalogue.serializers import (
    ProductCategoryReadSerializer,
    ProductReadSerializer,
    ReviewSerializer,
    CountrySerializer
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
    get=extend_schema(
        tags=['Product Filter'],
        summary="List all countries",
        description="Retrieve a list of all countries along with their icons.",
        parameters=common_parameters
    )
)
class CountryListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data)



@extend_schema_view(
    list=extend_schema(
        # tags=['Category and Product'],
        tags=['Product Filter'],
        summary="List product categories",
        description="Retrieve a list of all product categories that are available.",
        parameters=common_parameters
        # parameters=common_parameters + [
        #     OpenApiParameter(
        #         name='is_wholesale',
        #         type=bool,
        #         required=False,
        #         description="Filter to show products for wholesale (true) or retail (false)."
        #     )
        # ],
    ),
    retrieve=extend_schema(
        tags=['Category and Product'],
        summary="Retrieve a product category",
        description="Retrieve a specific product category by ID.",
        parameters=common_parameters
        # parameters=common_parameters + [
        #     OpenApiParameter(
        #         name='is_wholesale',
        #         type=bool,
        #         required=False,
        #         description="Filter to show products for wholesale (true) or retail (false)."
        #     )
        # ],
    ),
)
class ProductCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and Retrieve product categories
    """

    # queryset = Category.objects.browsable()
    serializer_class = ProductCategoryReadSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        language = get_language()
        user = self.request.user if self.request.user.is_authenticated else None
        is_wholesale = True if user and user.is_vendor else (False if user else None)
        queryset = Category.objects.browsable(user=user, is_wholesale=is_wholesale)
        if language == 'ar':
            queryset = queryset.filter(name_ar__isnull=False)
        else:
            queryset = queryset.filter(name_en__isnull=False)
        return queryset


@extend_schema_view(
    list=extend_schema(
        tags=['Category and Product'],
        summary=_("List products"),
        description=_("Retrieve a list of all products that are available."),
        parameters=[
            *common_parameters,
            OpenApiParameter(
                name='is_wholesale',
                location=OpenApiParameter.QUERY,
                required=False,
                description=_("Filter products by wholesale (true) or retail (false)."),
                type=str,  # or type=bool if your library supports it
                examples=[
                    OpenApiExample("Wholesale", value="true"),
                    OpenApiExample("Retail", value="false"),
                ]
            ),
        ],
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
    List and Retrieve products
    """

    serializer_class = ProductReadSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        language = get_language()
        user = self.request.user if self.request.user.is_authenticated else None
        is_wholesale = True if user and user.is_vendor else (False if user else None)
        
        queryset = Product.objects.browsable(user=user, is_wholesale=is_wholesale).prefetch_related(
            'categories', 'source_country', 'specifications', 'recommended_products', 'review_set'
        )

        if language == 'ar':
            return queryset.filter(title_ar__isnull=False)
        else:
            return queryset.filter(title_en__isnull=False)
# class ProductViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     List and Retrieve product
#     """

#     queryset = Product.objects.browsable().prefetch_related('categories', 'source_country', 'specifications', 'recommended_products', 'review_set')
#     serializer_class = ProductReadSerializer
#     permission_classes = (permissions.AllowAny,)

#     def get_queryset(self):
#         language = get_language()
            
        # order_by,
        # only_discounted=only_discounted

#         queryset = super().get_queryset()

#         if language == 'ar':
#             return queryset.filter(title_ar__isnull=False)
#         else:
#             return queryset.filter(title_en__isnull=False)
            # only_discounted = self.request.query_params.get('only_discounted') == 'true'
            # order_by = self.request.query_params.get('order_by')



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
        OpenApiParameter(name='only_discounted', description=_('Filter only discounted products (true or false)'), required=False, type=bool),        
        OpenApiParameter(
            name='order_by',
            description=_('Sort the products by price, date_added, or rating. Options: "price_asc", "price_desc", "date_added", "rating"'),
            required=False, type=str,
            examples=[
                OpenApiExample("Price ascending", value="price_asc"),
                OpenApiExample("Price descending", value="price_desc"),
                OpenApiExample("Highest Discount", value="discount_desc"),
                OpenApiExample("Lowest Discount", value="discount_asc"),
                OpenApiExample("Date added", value="date_added"),
                OpenApiExample("Rating", value="rating"),
            ]
        ),
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
        

        user = self.request.user if self.request.user.is_authenticated else None
        is_wholesale = True if user and user.is_vendor else (False if user else None)

        queryset = Product.objects.browsable(user=user, is_wholesale=is_wholesale).filter_products(
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






@extend_schema(
    tags=['Product Filter'],
    summary=_("search products"),
    description=_("search products based on various criteria such as country, price range, category, and more."),
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
        OpenApiParameter(name='q', description=_('Search query for the product title or description'), required=False, type=str),
    ],
    responses={200: ProductReadSerializer(many=True)},
)
class ProductSearchView(generics.ListAPIView):
    serializer_class = ProductReadSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '').strip()
        language = self.request.headers.get('Accept-Language', 'en')
        user = self.request.user

        results = SearchQuerySet().models(Product)

        if query:
            q_objects = Q()
            if language == 'ar':
                q_objects |= Q(title_ar__icontains=query) | Q(title_ar__fuzzy=query) 
                q_objects |= Q(description_ar__icontains=query) | Q(description_ar__fuzzy=query)
            else:
                q_objects |= Q(title_en__icontains=query) | Q(title_en__fuzzy=query) 
                q_objects |= Q(description_en__icontains=query) | Q(description_en__fuzzy=query)

            results = results.filter(q_objects)

        product_ids = [int(result.pk.split('.')[-1]) for result in results]

        return Product.objects.browsable(user=user).filter(id__in=product_ids)


    # def get_queryset(self):
    #     query = self.request.query_params.get('q', '').strip()
    #     language = self.request.headers.get('Accept-Language', 'en')

    #     results = SearchQuerySet().models(Product)

    #     if query:
    #         q_objects = Q()
    #         if language == 'ar':
    #             q_objects |= Q(title_ar__icontains=query)
    #             q_objects |= Q(description_ar__icontains=query)
    #         else:
    #             q_objects |= Q(title_en__icontains=query)
    #             q_objects |= Q(description_en__icontains=query)

    #         results = results.filter(q_objects)

    #     product_ids = [int(result.pk.split('.')[-1]) for result in results]

    #     return Product.objects.filter(id__in=product_ids, is_public=True)



@extend_schema(
    tags=['Product Filter'],
    summary=_("search categories"),
    description=_("search categories based on various criteria."),
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
        OpenApiParameter(name='q', description=_('Search query for the category name or description'), required=False, type=str),
    ],
    responses={200: ProductCategoryReadSerializer(many=True)},
)
class CategorySearchView(generics.ListAPIView):
    serializer_class = ProductCategoryReadSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '').strip()
        language = self.request.headers.get('Accept-Language', 'en')
        user = self.request.user

        results = SearchQuerySet().models(Category)
        if query:
            q_objects = Q()
            if language == 'ar':
                q_objects |= Q(name_ar__icontains=query) | Q(name_ar__fuzzy=query)
                q_objects |= Q(description_ar__icontains=query) | Q(description_ar__fuzzy=query)
            else:
                q_objects |= Q(name_en__icontains=query) | Q(name_en__fuzzy=query)
                q_objects |= Q(description_en__icontains=query) | Q(description_en__fuzzy=query)

            results = results.filter(q_objects)

        category_ids = [int(result.pk.split('.')[-1]) for result in results]

        return Category.objects.browsable(user=user).filter(id__in=category_ids)
