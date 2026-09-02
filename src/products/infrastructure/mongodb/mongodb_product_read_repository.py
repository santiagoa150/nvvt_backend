from typing import List, Optional, cast

from motor.motor_asyncio import AsyncIOMotorCollection

from products.domain.product import Product
from products.domain.product_dict import ProductDict
from products.domain.repository.product_read_repository import ProductReadRepository
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.str_value_object import StringValueObject


class MongoDBProductReadRepository(ProductReadRepository):
    """MongoDB implementation of the ProductReadRepository interface for reading product data."""

    def __init__(self, collection: AsyncIOMotorCollection):
        """Initializes the MongoDBProductReadRepository with a MongoDB collection."""
        self._collection = collection

    async def get_product_by_id(self, product_id: IdValueObject) -> Optional[Product]:
        """Retrieves a product by its ID."""
        document = await self._collection.find_one({"product_id": product_id.str})

        if document is None:
            return None

        return Product.from_dict(cast(ProductDict, document))

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

    async def exists_by_campaign_and_code(
        self, campaign_id: IdValueObject, code: StringValueObject
    ) -> bool:
        """Check if a product with the given code already exists for the campaign."""
        document = await self._collection.find_one(
            {"campaign_id": campaign_id.str, "code": code.str}
        )
        return document is not None

    async def get_product_by_campaign_and_code(
        self, campaign_id: IdValueObject, code: StringValueObject
    ) -> Optional[Product]:
        """Retrieves a product by its campaign and code."""
        document = await self._collection.find_one(
            {"campaign_id": campaign_id.str, "code": code.str}
        )

        if document is None:
            return None

        return Product.from_dict(cast(ProductDict, document))
