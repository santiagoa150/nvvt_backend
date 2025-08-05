from motor.motor_asyncio import AsyncIOMotorCollection

from orders.application.query.get_order_by_id.get_order_by_id_query import GetOrderByIdQuery
from orders.application.query.get_order_by_id.get_order_by_id_query_handler import GetOrderByIdQueryHandler
from orders.domain.order import Order
from orders.infrastructure.mongodb.mongodb_order_constants import MongoDBOrderConstants
from orders.infrastructure.mongodb.mongodb_order_read_repository import MongoDBOrderReadRepository
from orders.infrastructure.mongodb.mongodb_order_schema import create_order_indexes
from orders.infrastructure.mongodb.mongodb_order_write_repository import MongoDBOrderWriteRepository
from shared import get_mongo_client
from shared.domain.cqrs.query.query_handler import query_handler

_orders_collection: AsyncIOMotorCollection | None = None
_mongo_order_read_repository: MongoDBOrderReadRepository | None = None
_mongo_order_write_repository: MongoDBOrderWriteRepository | None = None


async def get_clients_collection() -> AsyncIOMotorCollection:
    """Returns the orders collection from the MongoDB client."""

    global _orders_collection

    if _orders_collection is None:
        client = get_mongo_client()
        _orders_collection = client.db[MongoDBOrderConstants.COLLECTION_NAME.value]
        await create_order_indexes(_orders_collection)

    return _orders_collection


async def create_mongodb_order_read_repository() -> MongoDBOrderReadRepository:
    """Creates an instance of MongoDBOrderReadRepository."""

    global _mongo_order_read_repository

    if _mongo_order_read_repository is None:
        _mongo_order_read_repository = MongoDBOrderReadRepository(await get_clients_collection())

    return _mongo_order_read_repository


async def create_mongodb_order_write_repository() -> MongoDBOrderWriteRepository:
    """Creates an instance of MongoDBOrderWriteRepository."""

    global _mongo_order_write_repository

    if _mongo_order_write_repository is None:
        _mongo_order_write_repository = MongoDBOrderWriteRepository(await get_clients_collection())

    return _mongo_order_write_repository


@query_handler(GetOrderByIdQuery)
async def get_order_by_id_query_handler():
    """Creates a query handler for GetOrderByIdQuery."""

    repository = await create_mongodb_order_read_repository()
    return GetOrderByIdQueryHandler(repository)
