from collections.abc import Awaitable
from typing import Any, Dict, Type, TypeVar

from shared.domain.cqrs.query.iquery import IQuery
from shared.domain.cqrs.query.iquery_handler import IQueryHandler
from shared.domain.exceptions.cqrs_exception import CqrsException

Query = TypeVar("Query", bound=IQuery)


class QueryBus:
    """QueryBus is responsible for dispatching queries to their respective handlers."""

    def __init__(self):
        self._handlers: Dict[Type[IQuery], IQueryHandler] = {}

    def register_handler(self, query: Type[Query], handler: IQueryHandler[Query]):
        """
        Register a query handler for a specific query type.
        :param query: The query type that the handler will handle.
        :param handler: The handler class that will process the query.
        """

        if not issubclass(query, IQuery):
            raise CqrsException.invalid_query_sub_class(query)

        if query not in self._handlers:
            self._handlers[query] = handler

    def query(self, query: IQuery) -> Awaitable[Any]:
        """
        Dispatch a query to its handler and return the result.
        :param query: The query to be handled.
        """

        query_type = type(query)

        if query_type not in self._handlers:
            raise CqrsException.query_not_registered(str(query_type))

        handler = self._handlers[query_type]

        return handler.handle(query)
