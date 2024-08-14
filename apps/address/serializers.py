from rest_framework import serializers
from address.models import UserAddress

class AddressSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize the UserAddress model
    """

    user = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:
        model = UserAddress
        fields = "__all__"
        read_only_fields = ["user"]
