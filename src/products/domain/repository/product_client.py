from abc import ABC, abstractmethod
from typing import List

from products.domain.cart_item import CartItem
from products.domain.product_provider import ProductProvider
from products.domain.scraped_product import ScrapedProduct
from shared.domain.value_objects.int_value_object import IntValueObject
from shared.domain.value_objects.str_value_object import StringValueObject


class ProductClient(ABC):
    """Interface for a client that fetches product data from an external provider."""

    @abstractmethod
    async def build_product(
        self, provider: ProductProvider, code: StringValueObject, campaign_number: IntValueObject
    ) -> ScrapedProduct:
        """
        Fetch a product's data from the provided product provider.

        :param provider: The product provider containing the provider's bearer token.
        :param code: The code of the product to fetch.
        :param campaign_number: The number of the campaign the product belongs to.
        :return: A ScrapedProduct instance representing the fetched product data.
        """
        pass

    @abstractmethod
    async def get_cart_items(
        self, provider: ProductProvider, cart_id: StringValueObject
    ) -> List[CartItem]:
        """
        Fetch every line item within the given cart.

        :param provider: The product provider containing the provider's bearer token.
        :param cart_id: The ID of the cart to fetch.
        :return: A list of CartItem instances representing each product and quantity in the cart.
        """
        pass
