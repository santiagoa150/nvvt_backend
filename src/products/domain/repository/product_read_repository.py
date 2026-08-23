from abc import ABC, abstractmethod
from typing import List

from products.domain.product import Product
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.str_value_object import StringValueObject


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

    @abstractmethod
    async def exists_by_campaign_and_code(
        self, campaign_id: IdValueObject, code: StringValueObject
    ) -> bool:
        """
        Check if a product with the given code already exists for the campaign.

        :param campaign_id: The ID of the campaign to check.
        :param code: The code of the product to check.
        :return: True if the product exists, False otherwise.
        """
        pass
