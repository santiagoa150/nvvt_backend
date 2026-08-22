from abc import ABC, abstractmethod
from typing import List

from products.domain.product import Product
from shared.domain.value_objects.id_value_object import IdValueObject


class ProductReadRepository(ABC):
    """Abstract base class for product reading repository operations."""

    @abstractmethod
    async def get_products_by_campaign_id(self, campaign_id: IdValueObject) -> List[Product]:
        """
        Retrieve all products belonging to a campaign.

        :param campaign_id: The ID of the campaign to retrieve products for.
        :return: A list of products belonging to the campaign.
        """
        pass

    @abstractmethod
    async def get_products_by_ids(self, product_ids: List[IdValueObject]) -> List[Product]:
        """
        Retrieve products matching the given IDs.

        :param product_ids: The IDs of the products to retrieve.
        :return: A list of matching products.
        """
        pass
