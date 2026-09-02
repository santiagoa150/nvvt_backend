from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCollection

from notifications.application.command import (
    MarkNotificationsAsSeenCommand,
    MarkNotificationsAsSeenCommandHandler,
    SendNotificationCommand,
    SendNotificationCommandHandler,
)
from notifications.application.query import (
    GetPaginatedNotificationsQuery,
    GetPaginatedNotificationsQueryHandler,
)
from notifications.infrastructure.broker.in_memory_notification_broker import (
    InMemoryNotificationBroker,
)
from notifications.infrastructure.mongodb.mongodb_notification_constants import (
    MongoDBNotificationConstants,
)
from notifications.infrastructure.mongodb.mongodb_notification_read_repository import (
    MongoDBNotificationReadRepository,
)
from notifications.infrastructure.mongodb.mongodb_notification_schema import (
    create_notification_indexes,
)
from notifications.infrastructure.mongodb.mongodb_notification_write_repository import (
    MongoDBNotificationWriteRepository,
)
from shared import get_mongo_client
from shared.domain.cqrs.command.command_handler import command_handler
from shared.domain.cqrs.query.query_handler import query_handler

_notification_broker: Optional[InMemoryNotificationBroker] = None
_notifications_collection: Optional[AsyncIOMotorCollection] = None
_mongo_notification_write_repository: Optional[MongoDBNotificationWriteRepository] = None
_mongo_notification_read_repository: Optional[MongoDBNotificationReadRepository] = None


def get_notification_broker() -> InMemoryNotificationBroker:
    """Returns the singleton in-memory notification broker."""

    global _notification_broker

    if _notification_broker is None:
        _notification_broker = InMemoryNotificationBroker()

    return _notification_broker


async def get_notifications_collection() -> AsyncIOMotorCollection:
    """Returns the notifications collection from the MongoDB client."""

    global _notifications_collection

    if _notifications_collection is None:
        client = get_mongo_client()
        _notifications_collection = client.db[MongoDBNotificationConstants.COLLECTION_NAME.value]
        await create_notification_indexes(_notifications_collection)

    return _notifications_collection


async def create_mongodb_notification_write_repository() -> MongoDBNotificationWriteRepository:
    """Creates an instance of MongoDBNotificationWriteRepository."""

    global _mongo_notification_write_repository

    if _mongo_notification_write_repository is None:
        _mongo_notification_write_repository = MongoDBNotificationWriteRepository(
            await get_notifications_collection()
        )

    return _mongo_notification_write_repository


async def create_mongodb_notification_read_repository() -> MongoDBNotificationReadRepository:
    """Creates an instance of MongoDBNotificationReadRepository."""

    global _mongo_notification_read_repository

    if _mongo_notification_read_repository is None:
        _mongo_notification_read_repository = MongoDBNotificationReadRepository(
            await get_notifications_collection()
        )

    return _mongo_notification_read_repository


@command_handler(SendNotificationCommand)
async def create_send_notification_command_handler() -> SendNotificationCommandHandler:
    """Creates a command handler for SendNotificationCommand."""

    write_repository = await create_mongodb_notification_write_repository()
    broker = get_notification_broker()
    return SendNotificationCommandHandler(write_repository, broker)


@query_handler(GetPaginatedNotificationsQuery)
async def create_get_paginated_notifications_query_handler() -> (
    GetPaginatedNotificationsQueryHandler
):
    """Creates a query handler for GetPaginatedNotificationsQuery."""

    repository = await create_mongodb_notification_read_repository()
    return GetPaginatedNotificationsQueryHandler(repository)


@command_handler(MarkNotificationsAsSeenCommand)
async def create_mark_notifications_as_seen_command_handler() -> (
    MarkNotificationsAsSeenCommandHandler
):
    """Creates a command handler for MarkNotificationsAsSeenCommand."""

    write_repository = await create_mongodb_notification_write_repository()
    return MarkNotificationsAsSeenCommandHandler(write_repository)
