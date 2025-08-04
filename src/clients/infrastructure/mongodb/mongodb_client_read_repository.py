from motor.motor_asyncio import AsyncIOMotorCollection

from clients.domain.repository.client_read_repository import ClientReadRepository


class MongoDBClientReadRepository(ClientReadRepository):
    """MongoDB implementation of the ClientReadRepository interface for reading client data."""

    def __init__(self, collection: AsyncIOMotorCollection):
        """Initializes the MongoDBClientReadRepository with a MongoDB collection."""
        self._collection = collection
