from django.urls import include, path

from customer.views import (
    UserRegisterationAPIView,
    UserLoginAPIView,
)

urlpatterns = [
    path("register/", UserRegisterationAPIView.as_view(), name="user_register"),
    path("login/", UserLoginAPIView.as_view(), name="user_login"),
    path("order/", include("order.urls", namespace="order")),
    path("user/", include("customer.urls", namespace="user")),
    path("address/", include("address.urls", namespace="addresse")),
    path("catalogue/", include("catalogue.urls", namespace="catalogue")),
    path("basket/", include("basket.urls", namespace="basket")),
]
