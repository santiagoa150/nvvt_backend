from motor.motor_asyncio import AsyncIOMotorCollection

from clients.infrastructure.mongodb.mongodb_client_constants import MongoDBClientConstants
from clients.infrastructure.mongodb.mongodb_client_read_repository import MongoDBClientReadRepository
from clients.infrastructure.mongodb.mongodb_client_schema import create_client_indexes
from clients.infrastructure.mongodb.mongodb_client_write_repository import MongoDBClientWriteRepository
from shared import get_mongo_client

_clients_collection: AsyncIOMotorCollection | None = None
_mongo_client_read_repository: MongoDBClientReadRepository | None = None
_mongo_client_write_repository: MongoDBClientWriteRepository | None = None


async def get_clients_collection() -> AsyncIOMotorCollection:
    """Returns the clients collection from the MongoDB client."""

    global _clients_collection

    if _clients_collection is None:
        client = get_mongo_client()
        _clients_collection = client.db[MongoDBClientConstants.COLLECTION_NAME.value]
        await create_client_indexes(_clients_collection)

    return _clients_collection


async def create_mongodb_client_read_repository() -> MongoDBClientReadRepository:
    """Creates an instance of MongoDBClientReadRepository."""

    global _mongo_client_read_repository

    if _mongo_client_read_repository is None:
        _mongo_client_read_repository = MongoDBClientReadRepository(await get_clients_collection())

    return _mongo_client_read_repository


async def create_mongodb_client_write_repository() -> MongoDBClientWriteRepository:
    """Creates an instance of MongoDBClientWriteRepository."""

    global _mongo_client_write_repository

    if _mongo_client_write_repository is None:
        _mongo_client_write_repository = MongoDBClientWriteRepository(await get_clients_collection())

    return _mongo_client_write_repository
