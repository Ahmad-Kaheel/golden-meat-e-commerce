from django.db.models import Avg
from django.db import models
from django.utils.translation import get_language
from modeltranslation.utils import get_translation_fields


class CategoryQuerySet(models.QuerySet):
    def browsable(self, user=None, is_wholesale=None):
        """
        Excludes non-public categories.
        - If user is provided, include categories based on user type.
        """
        queryset = self.filter(is_public=True)

        if is_wholesale is not None:
            queryset = queryset.filter(is_wholesale=is_wholesale)

        elif user and user.is_authenticated and user.is_vendor:
            queryset = queryset.filter(is_wholesale=True)

        return queryset



class ProductQuerySet(models.QuerySet):
    def browsable(self, user=None, is_wholesale=None):
        """
        Excludes non-public products and products with non-public categories.
        - If user is provided, include products based on user type.
        """
        queryset = self.filter(
            is_public=True,
            categories__is_public=True
        ).distinct()

        if user and user.is_authenticated:
            if user.is_vendor:
                queryset = queryset.filter(is_wholesale=True)
        else:
            if is_wholesale is not None:
                queryset = queryset.filter(is_wholesale=is_wholesale)

        return queryset


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
    
    def discounted(self):
        return self.filter(discount__gt=0)

    # sort
    def order_by_price_ascending(self):
        return self.order_by('price')

    def order_by_price_descending(self):
        return self.order_by('-price')

    def order_by_date_added(self):
        return self.order_by('-date_created')

    def order_by_rating(self):
        return self.order_by('-rating')

    def order_by_rating(self):
        return self.annotate(avg_rating=Avg('review__rating')).order_by('-avg_rating')
    
    def order_by_discount_desc(self):
        return self.order_by('-discount')

    def order_by_discount_asc(self):
        return self.order_by('discount')

    
    def filter_products(self, country_id=None, min_price=None,
                         max_price=None, category_id=None,
                         recommended_for=None, order_by=None,
                         only_discounted=False):
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
        if only_discounted:
            queryset = queryset.discounted()
        
        if order_by == 'price_asc':
            queryset = queryset.order_by_price_ascending()
        elif order_by == 'price_desc':
            queryset = queryset.order_by_price_descending()
        elif order_by == 'date_added':
            queryset = queryset.order_by_date_added()
        elif order_by == 'rating':
            queryset = queryset.order_by_rating()
        elif order_by == 'discount_desc':
            queryset = queryset.order_by_discount_desc()
        elif order_by == 'discount_asc':
            queryset = queryset.order_by_discount_asc()
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
