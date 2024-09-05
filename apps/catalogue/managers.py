from django.db import models
from django.utils.translation import get_language
from modeltranslation.utils import get_translation_fields

class CategoryQuerySet(models.QuerySet):
    def browsable(self):
        """
        Excludes non-public categories
        """
        return self.filter(is_public=True)


class ProductQuerySet(models.QuerySet):
    def browsable(self):
        """
        Excludes non-public products and products with non-public categories
        """
        return self.filter(
            is_public=True,
            categories__is_public=True
        ).distinct()


    def by_country(self, country_id):
        return self.filter(source_country=country_id)

    def by_price_range(self, min_price, max_price):
        return self.filter(price__gte=min_price, price__lte=max_price)

    def by_max_price(self, max_price):
        return self.filter(price__lte=max_price)

    def by_min_price(self, min_price):
        return self.filter(price__gte=min_price)

    def by_category(self, category_id):
        return self.filter(categories__id=category_id)

    def recommended_for(self, primary_product_id):
        return self.filter(primary_recommendations__primary_id=primary_product_id)

    def out_of_stock(self):
        return self.filter(quantity=0)

    def filter_products(self, country_id=None, min_price=None, max_price=None, category_id=None, recommended_for=None):
        queryset = self.all()
        if country_id is not None:
            queryset = queryset.by_country(country_id)
        if min_price is not None and max_price is not None:
            queryset = queryset.by_price_range(min_price, max_price)
        elif min_price is not None and max_price is None:
            queryset = queryset.by_min_price(min_price)
        elif min_price is None and max_price is not None:
            queryset = queryset.by_max_price(max_price)
        if category_id is not None:
            queryset = queryset.by_category(category_id)
        if recommended_for is not None:
            queryset = queryset.recommended_for(recommended_for)
        return queryset

    def translate_field(self, field_name):
        language = get_language()
        return f"{field_name}_{language}"

    def with_translations(self):
        """
        Annotates the queryset with translated fields for the current language
        """
        for model in self.model._meta.get_fields():
            if model.name in get_translation_fields(self.model):
                translated_field = self.translate_field(model.name)
                self = self.annotate(**{translated_field: models.F(f"{model.name}_{get_language()}")})
        return self
