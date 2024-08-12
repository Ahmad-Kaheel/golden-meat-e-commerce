from django.urls import include, path
from rest_framework.routers import DefaultRouter

from catalogue.views import ProductCategoryViewSet, ProductViewSet, ProductFilterAPIView

app_name = "catalogues"

router = DefaultRouter()
router.register(r"categories", ProductCategoryViewSet)
router.register(r"", ProductViewSet)
# router.register(r"products", ProductFilterAPIView)


urlpatterns = [
    path("filter/", ProductFilterAPIView.as_view(), name="product-filter"),
    path("", include(router.urls)),
]
