from typing import Optional
from basket.models import Basket
from basket.serializers import BasketItemsSerializer, BasketSerializer
from basket.basket import BasketService, clear_basket


class BasketOperationTypes:
    basket_add = 'add'
    item_add_quantity = 'add_quantity'
    item_minus_quantity = 'minus_quantity'
    basket_clear = 'clear'


class BasketMixin:
    """
    Mixin to handle basket operations using BasketService.
    """
    operation_type: Optional[str] = None
    __basket_service: Optional[BasketService] = None

    def _basket_add_item(self, request, product):
        self.reset_basket_option()
        self.__basket_service = BasketService(request.user)
        self.__basket_service.add(product)

    def _basket_add_item_quantity(self, request, product):
        self.reset_basket_option()
        self.__basket_service = BasketService(request.user)
        self.__basket_service.add_quantity(product)

    def _basket_minus_item_quantity(self, request, product):
        self.reset_basket_option()
        self.__basket_service = BasketService(request.user)
        self.__basket_service.minus_quantity(product)

    def _basket_clear(self, request):
        self.reset_basket_option()
        self.__basket_service = BasketService(request.user)
        self.__basket_service.clear()

    def clear_exist_basket(self, request):
        if request.user.is_authenticated:
            clear_basket(self.__basket_service.basket.id)

    def get_basket_data(self, request):
        """
        Returns basket data, including total amount and quantity.
        """
        self.reset_basket_option()
        self.__basket_service = BasketService(request.user)
        items = self.__basket_service.basket.items.all().select_related('product').distinct()
        items_serializer = BasketItemsSerializer(instance=items, many=True)
        basket_serializer = BasketSerializer(instance=self.__basket_service.basket)
        data = {
            'basket_id': self.__basket_service.basket.id,
            'basket': basket_serializer.data,
            'items': items_serializer.data,
            'total_amount': self.__basket_service.total_amount,
            'total_quantity_of_products': len(self.__basket_service)
        }
        return data

    def basket_operation(self, request, product=None):
        """
        Calls the appropriate method based on operation_type.
        """
        self.reset_basket_option()
        if self.operation_type == BasketOperationTypes.basket_add:
            self._basket_add_item(request, product)
        elif self.operation_type == BasketOperationTypes.item_add_quantity:
            self._basket_add_item_quantity(request, product)
        elif self.operation_type == BasketOperationTypes.item_minus_quantity:
            self._basket_minus_item_quantity(request, product)
        elif self.operation_type == BasketOperationTypes.basket_clear:
            self._basket_clear(request)

        return self.get_basket_data(request)

    def reset_basket_option(self):
        self.__basket_service = None
