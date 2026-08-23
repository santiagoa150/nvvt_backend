from motor.motor_asyncio import AsyncIOMotorCollection

from products.domain.product import Product
from products.domain.repository.product_write_repository import ProductWriteRepository


class MongoDBProductWriteRepository(ProductWriteRepository):
    """MongoDB implementation of the ProductWriteRepository interface for writing product data."""

    def __init__(self, collection: AsyncIOMotorCollection):
        """Initializes the MongoDBProductWriteRepository with a MongoDB collection."""
        self._collection = collection

    async def create_product(self, product: Product) -> None:
        """Creates a new product in the MongoDB collection."""
        await self._collection.insert_one(product.to_dict())
