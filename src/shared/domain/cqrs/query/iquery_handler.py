from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from shared.domain.cqrs.query.iquery import IQuery

Query = TypeVar("Query", bound=IQuery)

class IQueryHandler(ABC, Generic[Query]):
    """Interface for a query handler in the CQRS pattern."""

    @abstractmethod
    def handle(self, query: Query):
        """Handle the given query and return the result."""
        pass
