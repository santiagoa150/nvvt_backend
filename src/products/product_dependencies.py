from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCollection

from products.application.command import CreateProductCommand, CreateProductCommandHandler
from products.application.query import (
    GetProductsByCampaignQuery,
    GetProductsByCampaignQueryHandler,
    GetProductsByIdsQuery,
    GetProductsByIdsQueryHandler,
)
from products.infrastructure.mongodb.mongodb_product_constants import (
    MongoDBProductConstants,
)
from products.infrastructure.mongodb.mongodb_product_read_repository import (
    MongoDBProductReadRepository,
)
from products.infrastructure.mongodb.mongodb_product_schema import create_product_indexes
from products.infrastructure.mongodb.mongodb_product_write_repository import (
    MongoDBProductWriteRepository,
)
from products.infrastructure.novaventa.novaventa_product_client import (
    NovaventaProductClient,
)
from shared import get_mongo_client, get_query_bus
from shared.domain.cqrs.command.command_handler import command_handler
from shared.domain.cqrs.query.query_handler import query_handler

_products_collection: Optional[AsyncIOMotorCollection] = None
_mongo_product_read_repository: Optional[MongoDBProductReadRepository] = None
_mongo_product_write_repository: Optional[MongoDBProductWriteRepository] = None
_novaventa_product_client: Optional[NovaventaProductClient] = None


async def get_products_collection() -> AsyncIOMotorCollection:
    """Returns the products collection from the MongoDB client."""

    global _products_collection

    if _products_collection is None:
        client = get_mongo_client()
        _products_collection = client.db[MongoDBProductConstants.COLLECTION_NAME.value]
        await create_product_indexes(_products_collection)

    return _products_collection


async def create_mongodb_product_read_repository() -> MongoDBProductReadRepository:
    """Creates an instance of MongoDBProductReadRepository."""

    global _mongo_product_read_repository

    if _mongo_product_read_repository is None:
        _mongo_product_read_repository = MongoDBProductReadRepository(
            await get_products_collection()
        )

    return _mongo_product_read_repository


async def create_mongodb_product_write_repository() -> MongoDBProductWriteRepository:
    """Creates an instance of MongoDBProductWriteRepository."""

    global _mongo_product_write_repository

    if _mongo_product_write_repository is None:
        _mongo_product_write_repository = MongoDBProductWriteRepository(
            await get_products_collection()
        )

    return _mongo_product_write_repository


@query_handler(GetProductsByCampaignQuery)
async def create_get_products_by_campaign_query_handler() -> GetProductsByCampaignQueryHandler:
    """Creates a query handler for GetProductsByCampaignQuery."""

    repository = await create_mongodb_product_read_repository()
    return GetProductsByCampaignQueryHandler(repository)


@query_handler(GetProductsByIdsQuery)
async def create_get_products_by_ids_query_handler() -> GetProductsByIdsQueryHandler:
    """Creates a query handler for GetProductsByIdsQuery."""

    repository = await create_mongodb_product_read_repository()
    return GetProductsByIdsQueryHandler(repository)


async def create_novaventa_product_client() -> NovaventaProductClient:
    """Creates an instance of NovaventaProductClient."""

    global _novaventa_product_client

    if _novaventa_product_client is None:
        _novaventa_product_client = NovaventaProductClient()

    return _novaventa_product_client


@command_handler(CreateProductCommand)
async def create_create_product_command_handler() -> CreateProductCommandHandler:
    """Creates a command handler for CreateProductCommand."""

    query_bus = await get_query_bus()
    read_repository = await create_mongodb_product_read_repository()
    write_repository = await create_mongodb_product_write_repository()
    product_client = await create_novaventa_product_client()
    return CreateProductCommandHandler(query_bus, read_repository, write_repository, product_client)
