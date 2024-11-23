from rest_framework import serializers

from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language

from catalogue.models import (
    Product,
    Category,
    Review,
    ProductSpecification,
    Country
)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'icon']


class ProductCategoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'icon', 'description', 'created_at'
        ]

    def clean_text_field(self, value):
        return value.strip() if value else None

    def validate(self, data):
        data['name'] = self.clean_text_field(data.get('name'))
        data['description'] = self.clean_text_field(data.get('description'))
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['name'] = instance.name
        representation['description'] = instance.description
        return representation


class ProductReadSerializer(serializers.ModelSerializer):
    category_names = serializers.SerializerMethodField()
    specifications = serializers.SerializerMethodField()
    countries = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    recommended_products = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    price_with_discount = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'category_names',
            'specifications',
            'countries',
            'images',
            'recommended_products',
            'reviews',
            'price',
            'price_with_discount',
            'quantity',
            'discount',
            'is_public',
            'main_image_url',
            'rating',
            'description',
        )

    def get_category_names(self, obj):
        return [category.name for category in obj.categories.all()]

    def get_specifications(self, obj):
        language = get_language()
        specifications = []
        
        for spec in obj.specifications.all():
            if spec.predefined_name != 'other':
                if language == 'ar':
                    name = dict(ProductSpecification.PREDEFINED_NAME_CHOICES_AR).get(spec.predefined_name)
                    unit = dict(ProductSpecification.WEIGHT_UNIT_CHOICES_AR).get(spec.predefined_unit)
                elif language == 'en':
                    name = dict(ProductSpecification.PREDEFINED_NAME_CHOICES).get(spec.predefined_name)
                    unit = dict(ProductSpecification.WEIGHT_UNIT_CHOICES).get(spec.predefined_unit)
                else:
                    name = spec.predefined_name
                    unit = spec.predefined_unit
            else:
                name = spec.custom_name
                unit = spec.custom_unit
            
            specifications.append({
                "name": name,
                "unit": unit,
                "value": spec.custom_value,
            })
        
        return specifications

    def get_countries(self, obj):
        return [country.name for country in obj.source_country.all()]

    def get_images(self, obj):
        images = []
        
        if obj.main_image_url and hasattr(obj.main_image_url, 'url'):
            images.append({
                "url": obj.main_image_url.url,
                "alt_text": "Main image for product {}".format(obj.title),
            })
        
        for image in obj.images.all():
            if image.image_url and hasattr(image.image_url, 'url'):
                images.append({
                    "url": image.image_url.url,
                    "alt_text": image.alt_text,
                })
        
        return images


    def get_recommended_products(self, obj):
        return [
            {
                "id": recommendation.recommendation.id,
                "title": recommendation.recommendation.title,
                "ranking": recommendation.ranking
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
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = int(instance.pk)
        return representation



class ReviewSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()
    product_title = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id', 'user_email', 'product_title', 'product', 'rating', 
            'review', 'parent', 'replies', 'verified', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user_email', 'verified', 'product_title', 'created_at', 'updated_at']

    def get_user_email(self, obj):
        return obj.user.email

    def get_product_title(self, obj):
        return obj.product.title

    def get_replies(self, obj):
        replies = obj.reply.all()
        return ReviewSerializer(replies, many=True).data

    def clean_text_field(self, value):
        return value.strip() if value else None

    def validate(self, attrs):
        request = self.context.get('request')
        parent = attrs.get('parent')
        product = attrs.get('product')

        if request.method == 'POST':
            if parent and product and parent.product != product:
                raise serializers.ValidationError(_("The review must refer to the same product of the parent review."))

            if not parent and Review.objects.filter(user=request.user, product=product).exists():
                raise serializers.ValidationError(_("You can only create one review per product."))

        attrs['review'] = self.clean_text_field(attrs.get('review'))

        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation