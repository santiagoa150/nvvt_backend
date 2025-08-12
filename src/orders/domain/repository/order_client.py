from abc import ABC, abstractmethod

from orders.domain.product.product_provider import ProductProvider
from orders.domain.product.product import Product
from shared.domain.value_objects.str_value_object import StringValueObject


class OrderClient(ABC):
    """Interface for Order Client."""

    @abstractmethod
    async def build_product(self, provider: ProductProvider, product_url: StringValueObject) -> Product:
        """
        Build an order based on the provided order provider and product code.

        :param provider: The product provider containing session and route information.
        :param product_url: The URL of the product to order.
        :return: A Product instance representing the ordered product.
        """
        pass
