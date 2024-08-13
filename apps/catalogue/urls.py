from django.urls import include, path
from rest_framework.routers import DefaultRouter

from catalogue.views import ProductCategoryViewSet, ProductViewSet, ProductFilterAPIView, ReviewViewSet

app_name = "catalogue"

router = DefaultRouter()
router.register(r"categories", ProductCategoryViewSet)
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r"", ProductViewSet)


urlpatterns = [
    path("filter/", ProductFilterAPIView.as_view(), name="product-filter"),
    path("", include(router.urls)),
]