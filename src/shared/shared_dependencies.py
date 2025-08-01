from shared.infrastructure.cqrs.query.query_bus import QueryBus
from shared.infrastructure.cqrs.query.query_handler import get_registered_query_handlers

_query_bus: QueryBus | None = None


def get_query_bus() -> QueryBus:
    """
    This function initializes the QueryBus if it has not been created yet, and registers all query handlers.
    """

    global _query_bus

    if _query_bus is None:
        _query_bus = QueryBus()
        for query_type, handler_factory in get_registered_query_handlers().items():
            _query_bus.register_handler(query_type, handler_factory)

    return _query_bus
