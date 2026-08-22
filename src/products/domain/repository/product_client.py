from abc import ABC, abstractmethod

from products.domain.product_provider import ProductProvider
from products.domain.scraped_product import ScrapedProduct
from shared.domain.value_objects.str_value_object import StringValueObject


class ProductClient(ABC):
    """Interface for a client that fetches product data from an external provider."""

    @abstractmethod
    async def build_product(
        self, provider: ProductProvider, product_url: StringValueObject
    ) -> ScrapedProduct:
        """
        Fetch a product's data from the provided product provider and URL.

        :param provider: The product provider containing session and route information.
        :param product_url: The URL of the product to fetch.
        :return: A ScrapedProduct instance representing the fetched product data.
        """
        pass
