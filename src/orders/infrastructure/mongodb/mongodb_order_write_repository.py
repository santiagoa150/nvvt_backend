from motor.motor_asyncio import AsyncIOMotorCollection

from orders.domain.repository.order_write_repository import OrderWriteRepository


class MongoDBOrderWriteRepository(OrderWriteRepository):
    """MongoDB implementation of the OrderWriteRepository interface."""

    def __init__(self, collection: AsyncIOMotorCollection):
        """Initializes the MongoDBOrderWriteRepository with a MongoDB collection."""
        self._collection = collection
