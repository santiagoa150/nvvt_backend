from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCollection

from auth.application.command import (
    CreateUserCommand,
    CreateUserCommandHandler,
    LoginUserCommand,
    LoginUserCommandHandler,
    RefreshUserAuthTokensCommand,
    RefreshUserAuthTokensCommandHandler,
)
from auth.application.query import (
    GetActiveUserByEmailQuery,
    GetActiveUserByEmailQueryHandler,
    GetActiveUserByIdQuery,
    GetActiveUserByIdQueryHandler,
    VerifyUserAccessTokenQuery,
    VerifyUserAccessTokenQueryHandler,
)
from auth.infrastructure.jwt.jwt_token_repository import JwtTokenRepository
from auth.infrastructure.mongodb.mongodb_user_constants import MongoDBUserConstants
from auth.infrastructure.mongodb.mongodb_user_read_repository import (
    MongoDBUserReadRepository,
)
from auth.infrastructure.mongodb.mongodb_user_schema import create_user_indexes
from auth.infrastructure.mongodb.mongodb_user_write_repository import (
    MongoDBUserWriteRepository,
)
from shared import get_mongo_client, get_query_bus
from shared.domain.cqrs.command.command_handler import command_handler
from shared.domain.cqrs.query.query_handler import query_handler

_users_collection: Optional[AsyncIOMotorCollection] = None
_mongo_user_read_repository: Optional[MongoDBUserReadRepository] = None
_mongo_user_write_repository: Optional[MongoDBUserWriteRepository] = None
_jwt_token_repository: Optional[JwtTokenRepository] = None


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


async def get_jwt_token_repository() -> JwtTokenRepository:
    """Returns an instance of JwtTokenRepository."""

    global _jwt_token_repository

    if _jwt_token_repository is None:
        _jwt_token_repository = JwtTokenRepository()

    return _jwt_token_repository


@query_handler(GetActiveUserByEmailQuery)
async def create_get_active_user_by_email_query_handler() -> GetActiveUserByEmailQueryHandler:
    """Creates a query handler for GetActiveUserByEmailQuery."""

    repository = await create_mongodb_user_read_repository()
    return GetActiveUserByEmailQueryHandler(repository)


@command_handler(CreateUserCommand)
async def create_user_command_handler() -> CreateUserCommandHandler:
    """Handles the CreateUserCommand to create a new user."""

    read_repository = await create_mongodb_user_read_repository()
    write_repository = await create_mongodb_user_write_repository()

    return CreateUserCommandHandler(read_repository, write_repository)


@command_handler(LoginUserCommand)
async def create_login_user_command_handler() -> LoginUserCommandHandler:
    """Handles the LoginUserCommand to log in a user."""

    query_bus = await get_query_bus()
    token_repository = await get_jwt_token_repository()

    return LoginUserCommandHandler(query_bus, token_repository)


@query_handler(VerifyUserAccessTokenQuery)
async def create_verify_user_access_token_query_handler() -> VerifyUserAccessTokenQueryHandler:
    """Creates a query handler for VerifyUserAccessTokenQuery."""

    repository = await get_jwt_token_repository()
    return VerifyUserAccessTokenQueryHandler(repository)


@query_handler(GetActiveUserByIdQuery)
async def create_get_active_user_by_id_query_handler() -> GetActiveUserByIdQueryHandler:
    """Creates a query handler for GetActiveUserByIdQuery."""

    repository = await create_mongodb_user_read_repository()
    return GetActiveUserByIdQueryHandler(repository)


@command_handler(RefreshUserAuthTokensCommand)
async def create_refresh_user_auth_tokens_command_handler() -> RefreshUserAuthTokensCommandHandler:
    """Handles the RefreshUserAuthTokensCommand to refresh user authentication tokens."""

    query_bus = await get_query_bus()
    token_repository = await get_jwt_token_repository()

    return RefreshUserAuthTokensCommandHandler(query_bus, token_repository)
