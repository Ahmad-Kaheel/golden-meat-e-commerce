from django.urls import path, include
from rest_framework.routers import DefaultRouter

from order.views import (
    OrderAPIView, OrderPaypalPaymentComplete, 
    UserOrderListView, DeliverySettingsView, 
    UserOrderDetailView
)


app_name = "order"

urlpatterns = [
    # path('<int:order_id>/invoice/', order_invoice_view, name='order_invoice'),
    path('checkout/', OrderAPIView.as_view(), name='checkout'),
    path('<int:order_id>/',
         OrderPaypalPaymentComplete.as_view(),
         name='order_payment_complete'),
        path('my-orders/', UserOrderListView.as_view(), name='user-orders'),
        path('my-orders/<int:pk>/', UserOrderDetailView.as_view(), name='user-order-detail'),
        path('delivery-settings/', DeliverySettingsView.as_view(), name='delivery-settings'),
]
