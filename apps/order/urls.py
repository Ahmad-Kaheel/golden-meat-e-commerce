from django.urls import path, include
from rest_framework.routers import DefaultRouter

from order.views import OrderAPIView, OrderPaypalPaymentComplete


app_name = "order"

urlpatterns = [
    path('checkout/', OrderAPIView.as_view(), name='checkout'),
    path('order/<int:order_id>/',
         OrderPaypalPaymentComplete.as_view(),
         name='order_payment_complete'),
]
