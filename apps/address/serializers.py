from rest_framework import serializers

from address.models import UserAddress


class AddressReadOnlySerializer(serializers.ModelSerializer):
    """
    Serializer class to seralize Address model
    """

    user = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:
        model = UserAddress
        fields = "__all__"