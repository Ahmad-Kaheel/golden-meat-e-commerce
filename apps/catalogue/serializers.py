from rest_framework import serializers

from catalogue.models import (
    Product,
    Category,
    ProductImage,
    ProductCountry,
    ProductSpecification,
    ProductRecommendation
)



class ProductCategoryReadSerializer(serializers.ModelSerializer):
    """
    Serializer class for product categories
    """

    class Meta:
        model = Category
        fields = "__all__"


class ProductRecommendationReadSerializer(serializers.ModelSerializer):
    recommendation_title = serializers.CharField(source="recommendation.title", read_only=True)

    class Meta:
        model = ProductRecommendation
        fields = ("recommendation", "recommendation_title", "ranking")


class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = ['name', 'value']

class ProductCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCountry
        fields = ['country']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'



class ProductReadSerializer(serializers.ModelSerializer):
    """
    Serializer class for reading products
    """

    category = serializers.CharField(source="category.name", read_only=True)
    specifications = ProductSpecificationSerializer(many=True, read_only=True)
    countries = ProductCountrySerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    recommended_products = ProductRecommendationReadSerializer(source="primary_recommendations", many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'





# class ProductWriteSerializer(serializers.ModelSerializer):
#     category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.browsable())
#     images = serializers.PrimaryKeyRelatedField(queryset=ProductImage.objects.all(), many=True, required=False)
#     countries = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), many=True, required=False)
#     specifications = serializers.DictField(child=serializers.CharField(), required=False)
#     recommended_products = ProductRecommendationSerializer(many=True, required=False)

#     class Meta:
#         model = Product
#         fields = (
#             "title",
#             "description",
#             "price",
#             "quantity",
#             "is_public",
#             "category",
#             "main_image_url",
#             "parent",
#             "rating",
#             "images",
#             "countries",
#             "specifications",
#             "recommended_products",
#         )

#     def create(self, validated_data):
#         category = validated_data.pop("category")
#         images_data = validated_data.pop("images", [])
#         countries_data = validated_data.pop("countries", [])
#         specifications_data = validated_data.pop("specifications", {})
#         recommended_products_data = validated_data.pop("recommended_products", [])

#         product = Product.objects.create(**validated_data, category=category)

#         for image_id in images_data:
#             ProductImage.objects.create(product=product, image_url=image_id.image_url)

#         for country_id in countries_data:
#             ProductCountry.objects.create(product=product, country=country_id)

#         for spec_name, spec_value in specifications_data.items():
#             ProductSpecification.objects.create(product=product, name=spec_name, value=spec_value)

#         for recommendation_data in recommended_products_data:
#             ProductRecommendation.objects.create(
#                 primary=product,
#                 recommendation=recommendation_data['recommendation'],
#                 ranking=recommendation_data['ranking']
#             )

#         return product

#     def update(self, instance, validated_data):
#         if "category" in validated_data:
#             category = validated_data.pop("category")
#             instance.category = category

#         images_data = validated_data.pop("images", None)
#         countries_data = validated_data.pop("countries", None)
#         specifications_data = validated_data.pop("specifications", None)
#         recommended_products_data = validated_data.pop("recommended_products", None)

#         if images_data is not None:
#             instance.images.all().delete()
#             for image_id in images_data:
#                 ProductImage.objects.create(product=instance, image_url=image_id.image_url)

#         if countries_data is not None:
#             instance.countries.all().delete()
#             for country_id in countries_data:
#                 ProductCountry.objects.create(product=instance, country=country_id)

#         if specifications_data is not None:
#             instance.specifications.all().delete()
#             for spec_name, spec_value in specifications_data.items():
#                 ProductSpecification.objects.create(product=instance, name=spec_name, value=spec_value)

#         if recommended_products_data is not None:
#             instance.primary_recommendations.all().delete()
#             for recommendation_data in recommended_products_data:
#                 ProductRecommendation.objects.create(
#                     primary=instance,
#                     recommendation=recommendation_data['recommendation'],
#                     ranking=recommendation_data['ranking']
#                 )

#         return super().update(instance, validated_data)