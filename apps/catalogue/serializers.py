from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

from catalogue.models import (
    Product,
    Category,
    Review,
)



class ProductCategoryReadSerializer(serializers.ModelSerializer):
    """
    Serializer class for product categories
    """

    class Meta:
        model = Category
        fields = "__all__"


class ProductReadSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    specifications = serializers.SerializerMethodField()
    countries = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    recommended_products = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'category_name',
            'specifications',
            'countries',
            'images',
            'recommended_products',
            'reviews',
            'price',
            'description',
        )

    def get_specifications(self, obj):
        return [
            {
                "name": spec.name,
                "value": spec.value,
            }
            for spec in obj.specifications.all()
        ]

    def get_countries(self, obj):
        return [
            country.country.name
            for country in obj.countries.all()
        ]

    def get_images(self, obj):
        return [
            {
                "url": image.image_url.url,
                "alt_text": image.alt_text,
            }
            for image in obj.images.all()
        ]

    def get_recommended_products(self, obj):
        return [
            {
                "id": recommendation.recommendation.id,
                "title": recommendation.recommendation.title,
            }
            for recommendation in obj.primary_recommendations.all()
        ]

    def get_reviews(self, obj):
        return [
            {
                "user": review.user.email,
                "rating": review.rating,
                "review": review.review,
                "created_at": review.created_at,
                "updated_at": review.updated_at,
                "verified": review.verified,
                "replies": self.get_review_replies(review)
            }
            for review in obj.review_set.filter(parent=None)
        ]

    def get_review_replies(self, review):
        return [
            {
                "user": reply.user.email,
                "rating": reply.rating,
                "review": reply.review,
                "created_at": reply.created_at,
                "updated_at": reply.updated_at,
                "verified": reply.verified,
            }
            for reply in review.reply.all()
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()
    product_title = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id', 'user_email', 'product_title', 'product', 'rating', 
            'review', 'parent', 'verified', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user_email', 'verified', 'product_title', 'created_at', 'updated_at']

    def get_user_email(self, obj):
        return obj.user.email

    def get_product_title(self, obj):
        return obj.product.title

    def to_internal_value(self, data):
        if 'parent' in data and data['parent'] in [0, '0', '', None]:
            data['parent'] = None
        
        if data.get('parent') is not None:
            data.pop('rating', None)
        return super().to_internal_value(data)

    def validate(self, attrs):
        parent = attrs.get('parent')
        product = attrs.get('product')
        if parent and product and parent.product != product:
            raise serializers.ValidationError(_("The review must refer to the same product of the parent review."))
        return attrs

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating', instance.rating)
        instance.review = validated_data.get('review', instance.review)
        instance.save()
        return instance