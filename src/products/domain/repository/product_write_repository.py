from abc import ABC, abstractmethod

from products.domain.product import Product
from products.domain.scraped_product import ScrapedProduct
from shared.domain.value_objects.id_value_object import IdValueObject


class ProductWriteRepository(ABC):
    """Abstract base class for product writing repository operations."""

    @abstractmethod
    async def upsert_product(
        self, campaign_id: IdValueObject, scraped_product: ScrapedProduct
    ) -> Product:
        """
        Create a new product for the campaign, or refresh the existing one that shares
        the same campaign and code with the freshly scraped data.

        :param campaign_id: The ID of the campaign the product belongs to.
        :param scraped_product: The freshly scraped product data.
        :return: The persisted product, with its stable product_id.
        """
        pass
