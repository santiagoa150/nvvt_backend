from motor.motor_asyncio import AsyncIOMotorCollection

from clients.domain.client import Client
from clients.domain.repository.client_write_repository import ClientWriteRepository
from shared.domain.value_objects.id_value_object import IdValueObject


class MongoDBClientWriteRepository(ClientWriteRepository):
    """MongoDB implementation of the ClientWriteRepository interface for writing client data."""

    def __init__(self, collection: AsyncIOMotorCollection):
        """Initializes the MongoDBClientWriteRepository with a MongoDB collection."""
        self._collection = collection

    async def create_client(self, client: Client) -> None:
        """Create a new client."""
        await self._collection.insert_one(client.to_dict())

    async def delete_client(self, client_id: IdValueObject) -> bool:
        """Delete an existing client."""
        result = await self._collection.delete_one({"client_id": client_id.str})
        return result.deleted_count > 0

    async def update_client(self, client: Client) -> None:
        """Update an existing client."""
        update_data = dict(client.to_dict())
        update_data.pop("client_id", None)

        await self._collection.update_one(
            {"client_id": client.client_id.str}, {"$set": update_data}
        )
