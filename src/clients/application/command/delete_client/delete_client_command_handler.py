import logging

from clients.application.command import DeleteClientCommand
from clients.domain.client import Client
from clients.domain.repository.client_write_repository import ClientWriteRepository
from shared.domain.cqrs.command.icommand_handler import ICommandHandler
from shared.domain.exceptions.not_found_exception import NotFoundException


class DeleteClientCommandHandler(ICommandHandler[DeleteClientCommand]):
    """Command handler for deleting a client by its ID."""

    def __init__(self, repository: ClientWriteRepository):
        """
        :param repository: The client repository to use for deleting clients.
        """
        self._repository = repository
        self._logger = logging.getLogger(__name__)

    async def handle(self, command: DeleteClientCommand) -> None:
        """
        Handle the DeleteClientCommand to delete a client by its ID.
        :param command: The command containing the client ID.
        """
        self._logger.info(f'INIT :: Deleting client with ID: {command.client_id.str}')
        is_deleted = await self._repository.delete_client(command.client_id)
        if not is_deleted:
            raise NotFoundException.entity_not_found(Client.__name__, command.client_id.str)
