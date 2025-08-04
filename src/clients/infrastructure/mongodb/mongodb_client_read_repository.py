from typing import Optional, cast

from motor.motor_asyncio import AsyncIOMotorCollection

from clients.domain.client import Client
from clients.domain.client_dict import ClientDict
from clients.domain.repository.client_read_repository import ClientReadRepository
from shared.domain.pagination_dict import PaginationDict, empty_pagination_dict
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.pagination.limit_param import LimitParam
from shared.domain.value_objects.pagination.page_param import PageParam
from shared.infrastructure.mongodb.mongodb_utils import MongoDBUtils


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

    async def get_paginated_clients(self, page: PageParam, limit: LimitParam) -> PaginationDict[Client]:
        """Retrieves paginated clients from the MongoDB clients collection."""
        pipeline = MongoDBUtils.build_paginated_query(page, limit)
        result = await self._collection.aggregate(pipeline).to_list(length=1)
        aggregated = result[0]

        if not result or not aggregated:
            return empty_pagination_dict()

        clients = [Client.from_dict(cast(ClientDict, doc)) for doc in aggregated['data']]
        return PaginationDict(data=clients, metadata=aggregated['metadata'])
