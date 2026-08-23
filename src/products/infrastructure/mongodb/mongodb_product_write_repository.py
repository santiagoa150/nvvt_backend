from motor.motor_asyncio import AsyncIOMotorCollection

from products.domain.product import Product
from products.domain.repository.product_write_repository import ProductWriteRepository
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.positive_int_value_object import PositiveIntValueObject


class MongoDBProductWriteRepository(ProductWriteRepository):
    """MongoDB implementation of the ProductWriteRepository interface for writing product data."""

    def __init__(self, collection: AsyncIOMotorCollection):
        """Initializes the MongoDBProductWriteRepository with a MongoDB collection."""
        self._collection = collection

    async def create_product(self, product: Product) -> None:
        """Creates a new product in the MongoDB collection."""
        await self._collection.insert_one(product.to_dict())

    async def delete_product(self, product_id: IdValueObject) -> bool:
        """Deletes an existing product from the MongoDB collection."""
        result = await self._collection.delete_one({"product_id": product_id.str})
        return result.deleted_count > 0

    async def update_product_quantity(
        self, product_id: IdValueObject, quantity: PositiveIntValueObject
    ) -> None:
        """Updates the quantity of an existing product in the MongoDB collection."""
        await self._collection.update_one(
            {"product_id": product_id.str}, {"$set": {"quantity": quantity.int}}
        )
