from django.urls import include, path

from customer.views import (
    UserRegisterationAPIView,
    UserLoginAPIView,
)

urlpatterns = [
    path("register/", UserRegisterationAPIView.as_view(), name="user_register"),
    path("login/", UserLoginAPIView.as_view(), name="user_login"),
    path("user/", include("customer.urls", namespace="users")),
    path("address/", include("address.urls", namespace="addresses")),
    path("catalogue/", include("catalogue.urls", namespace="catalogues")),
]
