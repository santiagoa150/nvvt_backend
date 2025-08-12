from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCollection

from campaigns.application.command import CreateCampaignCommand, CreateCampaignCommandHandler, DeleteCampaignCommand, \
    DeleteCampaignCommandHandler
from campaigns.application.query import GetCampaignByIdQuery, GetCampaignByIdQueryHandler, GetPaginatedCampaignsQuery, \
    GetPaginatedCampaignsQueryHandler
from campaigns.domain.repository.campaign_read_repository import CampaignReadRepository
from campaigns.domain.repository.campaign_write_repository import CampaignWriteRepository
from campaigns.infrastructure.mongodb.mongodb_campaign_constants import MongoDBCampaignConstants
from campaigns.infrastructure.mongodb.mongodb_campaign_read_repository import MongoDBCampaignReadRepository
from campaigns.infrastructure.mongodb.mongodb_campaign_schema import create_campaign_indexes
from campaigns.infrastructure.mongodb.mongodb_campaign_write_repository import MongoDBCampaignWriteRepository
from shared import get_mongo_client
from shared.domain.cqrs.command.command_handler import command_handler
from shared.domain.cqrs.query.query_handler import query_handler

_campaigns_collection: Optional[AsyncIOMotorCollection] = None
_mongo_campaign_read_repository: Optional[MongoDBCampaignReadRepository] = None
_mongo_campaign_write_repository: Optional[MongoDBCampaignWriteRepository] = None


async def get_campaigns_collection() -> AsyncIOMotorCollection:
    """Returns the MongoDB collection for campaigns."""

    global _campaigns_collection

    if _campaigns_collection is None:
        client = get_mongo_client()
        _campaigns_collection = client.db[MongoDBCampaignConstants.COLLECTION_NAME.value]
        await create_campaign_indexes(_campaigns_collection)

    return _campaigns_collection


async def create_mongodb_campaign_read_repository() -> MongoDBCampaignReadRepository:
    """Creates an instance of MongoDBCampaignReadRepository."""

    global _mongo_campaign_read_repository

    if _mongo_campaign_read_repository is None:
        _mongo_campaign_read_repository = MongoDBCampaignReadRepository(await get_campaigns_collection())

    return _mongo_campaign_read_repository


async def create_mongodb_campaign_write_repository() -> MongoDBCampaignWriteRepository:
    """Creates an instance of MongoDBCampaignWriteRepository."""

    global _mongo_campaign_write_repository

    if _mongo_campaign_write_repository is None:
        _mongo_campaign_write_repository = MongoDBCampaignWriteRepository(await get_campaigns_collection())

    return _mongo_campaign_write_repository


@query_handler(GetCampaignByIdQuery)
async def create_get_campaign_by_id_query_handler() -> GetCampaignByIdQueryHandler:
    """
    Creates a query handler for GetCampaignByIdQuery.
    This function is decorated with `@query_handler` to register the handler with the query bus automatically.
    """
    repository: CampaignReadRepository = await create_mongodb_campaign_read_repository()
    return GetCampaignByIdQueryHandler(repository)


@query_handler(GetPaginatedCampaignsQuery)
async def create_get_paginated_campaigns_query_handler() -> GetPaginatedCampaignsQueryHandler:
    """
    Creates a query handler for GetPaginatedCampaignsQuery.
    This function is decorated with `@query_handler` to register the handler with the query bus automatically.
    """
    repository: CampaignReadRepository = await create_mongodb_campaign_read_repository()
    return GetPaginatedCampaignsQueryHandler(repository)


@command_handler(CreateCampaignCommand)
async def create_create_campaign_command_handler() -> CreateCampaignCommandHandler:
    """
    Creates a command handler for CreateCampaignCommand.
    This function is decorated with `@command_handler` to register the handler with the command bus automatically.
    """
    read_repository: CampaignReadRepository = await create_mongodb_campaign_read_repository()
    write_repository: CampaignWriteRepository = await create_mongodb_campaign_write_repository()
    return CreateCampaignCommandHandler(read_repository, write_repository)


@command_handler(DeleteCampaignCommand)
async def create_delete_campaign_command_handler() -> DeleteCampaignCommandHandler:
    """
    Creates a command handler for DeleteCampaignCommand.
    This function is decorated with `@command_handler` to register the handler with the command bus automatically.
    """
    write_repository: CampaignWriteRepository = await create_mongodb_campaign_write_repository()
    return DeleteCampaignCommandHandler(write_repository)
