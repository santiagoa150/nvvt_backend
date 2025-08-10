from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCollection

from orders.application.command.create_order.create_order_command import CreateOrderCommand
from orders.application.command.create_order.create_order_command_handler import CreateOrderCommandHandler
from orders.application.command.delete_order.delete_order_command import DeleteOrderCommand
from orders.application.command.delete_order.delete_order_command_handler import DeleteOrderCommandHandler
from orders.application.command.update_order_quantity.update_order_quantity_command import UpdateOrderQuantityCommand
from orders.application.command.update_order_quantity.update_order_quantity_command_handler import \
    UpdateOrderQuantityCommandHandler
from orders.application.query.get_order_by_id.get_order_by_id_query import GetOrderByIdQuery
from orders.application.query.get_order_by_id.get_order_by_id_query_handler import GetOrderByIdQueryHandler
from orders.application.query.get_orders_by_campaign.get_orders_by_campaign_query import GetOrdersByCampaignQuery
from orders.application.query.get_orders_by_campaign.get_orders_by_campaign_query_handler import \
    GetOrdersByCampaignQueryHandler
from orders.infrastructure.mongodb.mongodb_order_constants import MongoDBOrderConstants
from orders.infrastructure.mongodb.mongodb_order_read_repository import MongoDBOrderReadRepository
from orders.infrastructure.mongodb.mongodb_order_schema import create_order_indexes
from orders.infrastructure.mongodb.mongodb_order_write_repository import MongoDBOrderWriteRepository
from orders.infrastructure.novaventa.nova_venta_order_client import NovaVentaOrderClient
from shared import get_mongo_client, get_query_bus
from shared.domain.cqrs.command.command_handler import command_handler
from shared.domain.cqrs.query.query_handler import query_handler

_orders_collection: Optional[AsyncIOMotorCollection] = None
_mongo_order_read_repository: Optional[MongoDBOrderReadRepository] = None
_mongo_order_write_repository: Optional[MongoDBOrderWriteRepository] = None
_nova_venta_order_client: Optional[NovaVentaOrderClient] = None


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


async def create_nova_venta_order_client() -> NovaVentaOrderClient:
    """Creates an instance of NovaVentaOrderClient."""

    global _nova_venta_order_client

    if _nova_venta_order_client is None:
        _nova_venta_order_client = NovaVentaOrderClient()

    return _nova_venta_order_client


@query_handler(GetOrderByIdQuery)
async def get_order_by_id_query_handler():
    """Creates a query handler for GetOrderByIdQuery."""

    repository = await create_mongodb_order_read_repository()
    return GetOrderByIdQueryHandler(repository)


@query_handler(GetOrdersByCampaignQuery)
async def get_orders_by_campaign_query_handler():
    """Creates a query handler for GetOrdersByCampaignQuery."""

    repository = await create_mongodb_order_read_repository()
    return GetOrdersByCampaignQueryHandler(repository)


@command_handler(CreateOrderCommand)
async def create_order_command_handler():
    """Creates a command handler for CreateOrderCommand."""
    query_bus = await get_query_bus()
    write_repository = await create_mongodb_order_write_repository()
    order_client = await create_nova_venta_order_client()
    return CreateOrderCommandHandler(query_bus, write_repository, order_client)


@command_handler(DeleteOrderCommand)
async def delete_order_command_handler():
    """Creates a command handler for DeleteOrderCommand."""
    repository = await create_mongodb_order_write_repository()
    return DeleteOrderCommandHandler(repository)


@command_handler(UpdateOrderQuantityCommand)
async def update_order_quantity_command_handler():
    """Creates a command handler for UpdateOrderQuantityCommand."""
    query_bus = await get_query_bus()
    repository = await create_mongodb_order_write_repository()
    return UpdateOrderQuantityCommandHandler(query_bus, repository)
