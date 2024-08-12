from django.db import models


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
            category__is_public=True
        )
    
    def by_country(self, country_id):
        return self.filter(countries__country_id=country_id)
    
    def by_price_range(self, min_price, max_price):
        return self.filter(price__gte=min_price, price__lte=max_price)
    
    def by_max_price(self, max_price):
        return self.filter(price__lte=max_price)

    def by_min_price(self, min_price):
        return self.filter(price__gte=min_price)
    
    def by_category(self, category_id):
        return self.filter(category_id=category_id)
    
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