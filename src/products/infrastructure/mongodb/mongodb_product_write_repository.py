from typing import cast

from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import ReturnDocument

from products.domain.product import Product
from products.domain.product_dict import ProductDict
from products.domain.repository.product_write_repository import ProductWriteRepository
from products.domain.scraped_product import ScrapedProduct
from shared.domain.value_objects.id_value_object import IdValueObject


class MongoDBProductWriteRepository(ProductWriteRepository):
    """MongoDB implementation of the ProductWriteRepository interface for writing product data."""

    def __init__(self, collection: AsyncIOMotorCollection):
        """Initializes the MongoDBProductWriteRepository with a MongoDB collection."""
        self._collection = collection

    async def upsert_product(
        self, campaign_id: IdValueObject, scraped_product: ScrapedProduct
    ) -> Product:
        """Creates the product for this campaign and code, or refreshes it if it already exists."""
        document = await self._collection.find_one_and_update(
            {"campaign_id": campaign_id.str, "code": scraped_product.code.str},
            {
                "$set": {
                    "name": scraped_product.name.str,
                    "image_url": scraped_product.image_url.str,
                    "catalog_price": scraped_product.catalog_price.float,
                    "list_price": scraped_product.list_price.float,
                },
                "$setOnInsert": {
                    "product_id": IdValueObject.generate(),
                    "campaign_id": campaign_id.str,
                    "code": scraped_product.code.str,
                },
            },
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )
        return Product.from_dict(cast(ProductDict, document))
