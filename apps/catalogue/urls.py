from django.urls import include, path
from rest_framework.routers import DefaultRouter

from catalogue.views import (ProductCategoryViewSet, 
                             ProductViewSet, ProductSearchView, 
                             ProductFilterAPIView, ReviewViewSet,
                             CategorySearchView, CountryListView)

app_name = "catalogue"

router = DefaultRouter()
router.register(r"categories", ProductCategoryViewSet, basename='product-category')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r"", ProductViewSet, basename='product')


urlpatterns = [
    path('countries/', CountryListView.as_view(), name='country-list'),
    path("filter/", ProductFilterAPIView.as_view(), name="product-filter"),
    path('search/', ProductSearchView.as_view(), name='product-search'),
    path('search/categories/', CategorySearchView.as_view(), name='category_search'),
    path("", include(router.urls)),
]