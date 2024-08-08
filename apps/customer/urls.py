from django.urls import path
from customer.views import ProfileAPIView, UserAPIView

app_name = 'users'

urlpatterns = [
    path("", UserAPIView.as_view(), name="user_detail"),
    path("profile/", ProfileAPIView.as_view(), name="profile_detail"),
]
