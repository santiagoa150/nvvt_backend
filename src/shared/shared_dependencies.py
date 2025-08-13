from settings import settings
from shared.domain.cqrs.command.command_bus import CommandBus
from shared.domain.cqrs.command.command_handler import get_registered_command_handlers
from shared.domain.cqrs.query.query_bus import QueryBus
from shared.domain.cqrs.query.query_handler import get_registered_query_handlers
from shared.infrastructure.mongodb.mongodb_client import MongoDBClient

_query_bus: QueryBus | None = None
_command_bus: CommandBus | None = None
_mongo_client: MongoDBClient | None = None


async def get_query_bus() -> QueryBus:
    """
    This function initializes the QueryBus if it has not been created yet,
    and registers all query handlers.
    """

    global _query_bus

    if _query_bus is None:
        _query_bus = QueryBus()
        for query_type, handler_factory in get_registered_query_handlers().items():
            _query_bus.register_handler(query_type, await handler_factory())

    return _query_bus


async def get_command_bus() -> CommandBus:
    """
    This function initializes the CommandBus if it has not been created yet,
    and registers all command handlers.
    """

    global _command_bus

    if _command_bus is None:
        _command_bus = CommandBus()

        for command_type, handler_factory in get_registered_command_handlers().items():
            _command_bus.register_handler(command_type, await handler_factory())

    return _command_bus


def get_mongo_client() -> MongoDBClient:
    """
    This function initializes the MongoDBClient if it has not been created yet.
    It is used to manage the MongoDB connection throughout the application.
    """

    global _mongo_client

    if _mongo_client is None:
        _mongo_client = MongoDBClient(
            uri=str(settings.mongodb_uri),
            db_name=settings.mongodb_database,
        )

    return _mongo_client
