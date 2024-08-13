from django.contrib import admin

from catalogue.models import (
    Category,
    Product,
    ProductImage,
    ProductSpecification,
    ProductRecommendation,
    Country,
    ProductCountry,
    Review
)

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductSpecification)
admin.site.register(ProductRecommendation)
admin.site.register(Country)
admin.site.register(ProductCountry)
admin.site.register(Review)