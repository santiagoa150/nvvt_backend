from motor.motor_asyncio import AsyncIOMotorCollection

from orders.domain.repository.order_read_repository import OrderReadRepository


class MongoDBOrderReadRepository(OrderReadRepository):
    """MongoDB implementation of the OrderReadRepository interface."""

    def __init__(self, collection: AsyncIOMotorCollection):
        """Initializes the MongoDBOrderReadRepository with a MongoDB collection."""
        self._collection = collection
