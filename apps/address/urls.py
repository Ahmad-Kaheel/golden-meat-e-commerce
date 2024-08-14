from django.urls import path

from address.views import UserAddressAPIView

app_name = "addresse"

urlpatterns = [
        path('', UserAddressAPIView.as_view(), name='user-address'),
]