from typing import Type, Dict, TypeVar

from shared.infrastructure.cqrs.query.iquery import IQuery
from shared.infrastructure.cqrs.query.iquery_handler import IQueryHandler

Query = TypeVar("Query", bound=IQuery)

class QueryBus:
    """QueryBus is responsible for dispatching queries to their respective handlers."""

    def __init__(self):
        self._handlers: Dict[Type[IQuery], IQueryHandler] = {}

    def register_handler(self, query: Type[Query], handler: Type[IQueryHandler[Query]]):
        """
        Register a query handler for a specific query type.
        :param query: The query type that the handler will handle.
        :param handler: The handler class that will process the query.
        """

        if not issubclass(query, IQuery):
            raise TypeError(f"{query} must be subclass of IQuery")

        if query not in self._handlers:
            self._handlers[query] = handler()

    def query(self, query: IQuery):
        """
        Dispatch a query to its handler and return the result.
        :param query: The query to be handled.
        """

        query_type = type(query)

        if query_type not in self._handlers:
            raise Exception(f"{query_type} not registered in QueryBus")

        handler = self._handlers[query_type]

        return handler.handle(query)