from typing import NamedTuple, Optional

from django.db import models

from catalogue.models import Product
from basket.models import BasketItems, Basket


class BasketService:

    def __init__(self, user):
        self.user = user
        self.basket, created = Basket.objects.get_or_create(user=user)

    def add(self, product):
        basket_item, created = BasketItems.objects.get_or_create(
            basket=self.basket,
            product=product,
            defaults={
                'quantity': 1,
                'total_price': product.price_with_discount if product.discount else product.price
            }
        )
        if not created:
            basket_item.quantity += 1
            basket_item.total_price = basket_item.quantity * (product.price_with_discount if product.discount else product.price)
            basket_item.save()

    def remove(self, product):
        try:
            basket_item = BasketItems.objects.get(basket=self.basket, product=product)
            basket_item.delete()
        except BasketItems.DoesNotExist:
            pass

    def add_quantity(self, product):
        try:
            basket_item = BasketItems.objects.get(basket=self.basket, product=product)
            basket_item.quantity += 1
            basket_item.total_price = basket_item.quantity * (product.price_with_discount if product.discount else product.price)
            basket_item.save()
        except BasketItems.DoesNotExist:
            pass

    def minus_quantity(self, product):
        try:
            basket_item = BasketItems.objects.get(basket=self.basket, product=product)
            if basket_item.quantity > 1:
                basket_item.quantity -= 1
                basket_item.total_price = basket_item.quantity * (product.price_with_discount if product.discount else product.price)
                basket_item.save()
            else:
                basket_item.delete()
        except BasketItems.DoesNotExist:
            pass

    def __len__(self):
        return self.basket.items.aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0

    @property
    def total_amount(self):
        return self.basket.items.aggregate(total_price=models.Sum('total_price'))['total_price'] or 0

    def clear(self):
        self.basket.items.all().delete()

def clear_basket(basket_id):
    try:
        items = BasketItems.objects.filter(basket_id=basket_id)
        for item in items:
            print("inside for loop", item)
            item.delete()
        return True
    except Basket.DoesNotExist:
        return False