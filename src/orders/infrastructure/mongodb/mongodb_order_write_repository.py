from motor.motor_asyncio import AsyncIOMotorCollection

from orders.domain.order import Order
from orders.domain.repository.order_write_repository import OrderWriteRepository
from shared.domain.value_objects.id_value_object import IdValueObject


class MongoDBOrderWriteRepository(OrderWriteRepository):
    """MongoDB implementation of the OrderWriteRepository interface."""

    def __init__(self, collection: AsyncIOMotorCollection):
        """Initializes the MongoDBOrderWriteRepository with a MongoDB collection."""
        self._collection = collection

    async def create_order(self, order: Order) -> None:
        """Creates a new order in the MongoDB collection."""
        await self._collection.insert_one(order.to_dict())

    async def delete_order(self, order_id: IdValueObject) -> bool:
        """Deletes an existing order by its ID."""
        result = await self._collection.delete_one({"order_id": order_id.str})
        return result.deleted_count > 0
