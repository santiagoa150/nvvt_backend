from typing import Callable, Type, Awaitable

from shared.domain.cqrs.query.iquery import IQuery
from shared.domain.cqrs.query.iquery_handler import IQueryHandler

_handler_factories: dict[Type[IQuery], Awaitable[Callable[[], IQueryHandler[IQuery]]]] = {}

def query_handler(query_type: Type[IQuery]):
    """ Decorator to register a query handler factory for a specific query type."""
    def decorator(factory: Awaitable[Callable[[], IQueryHandler[IQuery]]]):
        _handler_factories[query_type] = factory
        return factory

    return decorator

def get_registered_query_handlers():
    """ Returns a dictionary of registered query handlers."""
    return _handler_factories.copy()
