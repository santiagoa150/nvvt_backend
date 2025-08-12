import logging

from clients.application.query.get.client_by_id.get_client_by_id_query import GetClientByIdQuery
from clients.domain.client import Client
from clients.domain.repository.client_read_repository import ClientReadRepository
from shared.domain.cqrs.query.iquery_handler import IQueryHandler
from shared.domain.exceptions.not_found_exception import NotFoundException


class GetClientByIdQueryHandler(IQueryHandler[GetClientByIdQuery]):
    """Handler for the GetClientByIdQuery."""

    def __init__(self, repository: ClientReadRepository):
        """
        :param repository: The client repository to use for fetching clients.
        """
        self._repository = repository
        self._logger = logging.getLogger(__name__)

    async def handle(self, query: GetClientByIdQuery) -> Client:
        """
        Handle the GetClientByIdQuery to retrieve a client by its ID.

        :param query: The query containing the client ID.
        :return: The client associated with the provided ID.
        :raises NotFoundException: If no client is found with the provided ID.
        """
        self._logger.info(f'INIT :: ClientID: {query.client_id.str}')
        client = await self._repository.get_client_by_id(query.client_id)

        if not client:
            raise NotFoundException.entity_not_found(Client.__name__, query.client_id.str)

        return client
