from typing import List, cast

from motor.motor_asyncio import AsyncIOMotorCollection

from products.domain.product import Product
from products.domain.product_dict import ProductDict
from products.domain.repository.product_read_repository import ProductReadRepository
from shared.domain.value_objects.id_value_object import IdValueObject


class MongoDBProductReadRepository(ProductReadRepository):
    """MongoDB implementation of the ProductReadRepository interface for reading product data."""

    def __init__(self, collection: AsyncIOMotorCollection):
        """Initializes the MongoDBProductReadRepository with a MongoDB collection."""
        self._collection = collection

    async def get_products_by_campaign_id(self, campaign_id: IdValueObject) -> List[Product]:
        """Retrieves all products belonging to a campaign."""
        documents = await self._collection.find({"campaign_id": campaign_id.str}).to_list(
            length=None
        )
        return [Product.from_dict(cast(ProductDict, document)) for document in documents]

    async def get_products_by_ids(self, product_ids: List[IdValueObject]) -> List[Product]:
        """Retrieves products matching the given IDs."""
        if not product_ids:
            return []

        documents = await self._collection.find(
            {"product_id": {"$in": [product_id.str for product_id in product_ids]}}
        ).to_list(length=None)
        return [Product.from_dict(cast(ProductDict, document)) for document in documents]
