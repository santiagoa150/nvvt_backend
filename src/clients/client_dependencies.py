from motor.motor_asyncio import AsyncIOMotorCollection

from clients.application.command.create_client.create_client_command import CreateClientCommand
from clients.application.command.create_client.create_client_command_handler import CreateClientCommandHandler
from clients.application.command.delete_client.delete_client_command import DeleteClientCommand
from clients.application.command.delete_client.delete_client_command_handler import DeleteClientCommandHandler
from clients.application.query.get_client_by_id.get_client_by_id_query import GetClientByIdQuery
from clients.application.query.get_client_by_id.get_client_by_id_query_handler import GetClientByIdQueryHandler
from clients.application.query.get_paginated_clients.get_paginated_clients_query import GetPaginatedClientsQuery
from clients.application.query.get_paginated_clients.get_paginated_clients_query_handler import \
    GetPaginatedClientsQueryHandler
from clients.infrastructure.mongodb.mongodb_client_constants import MongoDBClientConstants
from clients.infrastructure.mongodb.mongodb_client_read_repository import MongoDBClientReadRepository
from clients.infrastructure.mongodb.mongodb_client_schema import create_client_indexes
from clients.infrastructure.mongodb.mongodb_client_write_repository import MongoDBClientWriteRepository
from shared import get_mongo_client
from shared.domain.cqrs.command.command_handler import command_handler
from shared.domain.cqrs.query.query_handler import query_handler

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


@query_handler(GetClientByIdQuery)
async def create_get_client_by_id_query_handler():
    """Creates a query handler for GetClientByIdQuery."""

    repository = await create_mongodb_client_read_repository()
    return GetClientByIdQueryHandler(repository)


@query_handler(GetPaginatedClientsQuery)
async def create_get_paginated_clients_query_handler():
    """Creates a query handler for GetPaginatedClientsQuery."""

    repository = await create_mongodb_client_read_repository()
    return GetPaginatedClientsQueryHandler(repository)


@command_handler(CreateClientCommand)
async def create_create_client_command_handler():
    """Creates a command handler for CreateClientCommand."""

    repository = await create_mongodb_client_write_repository()
    return CreateClientCommandHandler(repository)


@command_handler(DeleteClientCommand)
async def create_delete_client_command_handler():
    """Creates a command handler for DeleteClientCommand."""

    repository = await create_mongodb_client_write_repository()
    return DeleteClientCommandHandler(repository)
