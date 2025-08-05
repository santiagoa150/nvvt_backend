from abc import ABC, abstractmethod

from orders.domain.order_provider import OrderProvider
from orders.domain.product import Product
from shared.domain.value_objects.string_value_object import StringValueObject


class OrderClient(ABC):
    """Interface for Order Client."""

    @abstractmethod
    async def build_product(self, provider: OrderProvider, product_url: StringValueObject) -> Product:
        """
        Build an order based on the provided order provider and product code.

        :param provider: The order provider containing session and route information.
        :param product_url: The URL of the product to order.
        :return: A Product instance representing the ordered product.
        """
        pass
