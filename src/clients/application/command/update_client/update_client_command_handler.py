import logging

from clients.application.command import UpdateClientCommand
from clients.application.query import GetClientByIdQuery
from clients.domain.client import Client
from clients.domain.repository.client_write_repository import ClientWriteRepository
from shared.domain.cqrs.command.icommand_handler import ICommandHandler
from shared.domain.cqrs.query.query_bus import QueryBus
from shared.domain.phone import Phone


class UpdateClientCommandHandler(ICommandHandler[UpdateClientCommand]):
    """Handler for the UpdateClientCommand."""

    def __init__(self, query_bus: QueryBus, write_repository: ClientWriteRepository):
        """
        :param write_repository: The client repository to use for updating clients.
        """
        self._query_bus = query_bus
        self._write_repository = write_repository
        self._logger = logging.getLogger(__name__)

    async def handle(self, command: UpdateClientCommand) -> None:
        """
        Handle the UpdateClientCommand to update an existing client.
        :param command: The command containing the client details.
        """
        self._logger.info(f"INIT :: Updating client with ID: {command.client_id.str}")

        client: Client = await self._query_bus.query(GetClientByIdQuery(command.client_id))

        if command.given_names is not None:
            client.given_names = command.given_names

        if command.family_names is not None:
            client.family_names = command.family_names

        if command.delivery_place is not None:
            client.delivery_place = command.delivery_place

        if command.phone_number is not None and command.country_phone_code is not None:
            client.phone = Phone.from_dict(
                {"country_code": command.country_phone_code.int, "number": command.phone_number.str}
            )

        await self._write_repository.update_client(client)
