from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCollection

from auth.application.command.create_user.create_user_command import CreateUserCommand
from auth.application.command.create_user.create_user_command_handler import CreateUserCommandHandler
from auth.infrastructure.mongodb.mongodb_user_constants import MongoDBUserConstants
from auth.infrastructure.mongodb.mongodb_user_read_repository import MongoDBUserReadRepository
from auth.infrastructure.mongodb.mongodb_user_schema import create_user_indexes
from auth.infrastructure.mongodb.mongodb_user_write_repository import MongoDBUserWriteRepository
from shared import get_mongo_client
from shared.domain.cqrs.command.command_handler import command_handler

_users_collection: Optional[AsyncIOMotorCollection] = None
_mongo_user_read_repository: Optional[MongoDBUserReadRepository] = None
_mongo_user_write_repository: Optional[MongoDBUserWriteRepository] = None


async def get_users_collection() -> AsyncIOMotorCollection:
    """Returns the users collection from the MongoDB client."""

    global _users_collection

    if _users_collection is None:
        client = get_mongo_client()
        _users_collection = client.db[MongoDBUserConstants.COLLECTION_NAME.value]
        await create_user_indexes(_users_collection)

    return _users_collection


async def create_mongodb_user_read_repository() -> MongoDBUserReadRepository:
    """Creates an instance of MongoDBUserReadRepository."""

    global _mongo_user_read_repository

    if _mongo_user_read_repository is None:
        _mongo_user_read_repository = MongoDBUserReadRepository(await get_users_collection())

    return _mongo_user_read_repository


async def create_mongodb_user_write_repository() -> MongoDBUserWriteRepository:
    """Creates an instance of MongoDBUserWriteRepository."""

    global _mongo_user_write_repository

    if _mongo_user_write_repository is None:
        _mongo_user_write_repository = MongoDBUserWriteRepository(await get_users_collection())

    return _mongo_user_write_repository


@command_handler(CreateUserCommand)
async def create_user_command_handler() -> CreateUserCommandHandler:
    """Handles the CreateUserCommand to create a new user."""

    read_repository = await create_mongodb_user_read_repository()
    write_repository = await create_mongodb_user_write_repository()

    return CreateUserCommandHandler(read_repository, write_repository)
