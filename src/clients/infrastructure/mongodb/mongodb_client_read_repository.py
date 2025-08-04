from typing import Optional, cast

from motor.motor_asyncio import AsyncIOMotorCollection

from clients.domain.client import Client
from clients.domain.client_dict import ClientDict
from clients.domain.repository.client_read_repository import ClientReadRepository
from shared.domain.value_objects.id_value_object import IdValueObject


class MongoDBClientReadRepository(ClientReadRepository):
    """MongoDB implementation of the ClientReadRepository interface for reading client data."""

    def __init__(self, collection: AsyncIOMotorCollection):
        """Initializes the MongoDBClientReadRepository with a MongoDB collection."""
        self._collection = collection

    async def get_client_by_id(self, client_id: IdValueObject) -> Optional[Client]:
        """Retrieves a client by its ID from the MongoDB collection."""
        document = await self._collection.find_one({'client_id': client_id.str})

        if document is None:
            return None

        return Client.from_dict(cast(ClientDict, document))
