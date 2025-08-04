from motor.motor_asyncio import AsyncIOMotorCollection

from clients.domain.client import Client
from clients.domain.repository.client_write_repository import ClientWriteRepository


class MongoDBClientWriteRepository(ClientWriteRepository):
    """MongoDB implementation of the ClientWriteRepository interface for writing client data."""

    def __init__(self, collection: AsyncIOMotorCollection):
        """Initializes the MongoDBClientWriteRepository with a MongoDB collection."""
        self._collection = collection

    async def create_client(self, client: Client) -> None:
        """Create a new client."""
        await self._collection.insert_one(client.to_dict())
