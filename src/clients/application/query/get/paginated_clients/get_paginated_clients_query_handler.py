import logging
from typing import Awaitable

from clients.application.query import GetPaginatedClientsQuery
from clients.domain.client import Client
from clients.domain.repository.client_read_repository import ClientReadRepository
from shared.domain.cqrs.query.iquery_handler import IQueryHandler
from shared.domain.pagination_dict import PaginationDict


class GetPaginatedClientsQueryHandler(IQueryHandler[GetPaginatedClientsQuery]):
    """Handler for the GetPaginatedClientsQuery."""

    def __init__(self, repository: ClientReadRepository):
        """
        :param repository: The client repository to use for fetching clients.
        """
        self._repository = repository
        self._logger = logging.getLogger(__name__)

    def handle(self, query: GetPaginatedClientsQuery) -> Awaitable[PaginationDict[Client]]:
        """
        Handle the GetPaginatedClientsQuery to retrieve paginated clients.
        :param query: The query containing pagination parameters.
        :return: A list of clients for the requested page.
        """
        self._logger.info(f'INIT :: Getting All Clients with Page: {query.page}, Limit: {query.limit}')
        return self._repository.get_paginated_clients(query.page, query.limit)
