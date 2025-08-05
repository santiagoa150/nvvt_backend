from motor.motor_asyncio import AsyncIOMotorCollection

from orders.domain.order import Order
from orders.domain.repository.order_write_repository import OrderWriteRepository


class MongoDBOrderWriteRepository(OrderWriteRepository):
    """MongoDB implementation of the OrderWriteRepository interface."""

    def __init__(self, collection: AsyncIOMotorCollection):
        """Initializes the MongoDBOrderWriteRepository with a MongoDB collection."""
        self._collection = collection

    async def create_order(self, order: Order) -> None:
        """Creates a new order in the MongoDB collection."""
        await self._collection.insert_one(order.to_dict())
