import logging

from clients.application.command.create_client.create_client_command import CreateClientCommand
from clients.domain.client import Client
from clients.domain.client_dict import ClientDict
from clients.domain.repository.client_write_repository import ClientWriteRepository
from shared.domain.cqrs.command.icommand_handler import ICommandHandler
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.phone_dict import PhoneDict


class CreateClientCommandHandler(ICommandHandler[CreateClientCommand]):
    """Handler for the CreateClientCommand."""

    def __init__(self, repository: ClientWriteRepository):
        """
        :param repository: The client repository to use for creating clients.
        """
        self._repository = repository
        self._logger = logging.getLogger(__name__)

    async def handle(self, command: CreateClientCommand) -> None:
        """
        Handle the CreateClientCommand to create a new client.
        :param command: The command containing the client details.
        """
        self._logger.info(
            f'INIT :: Creating Client with params: '
            f'- {command.given_names.str}, '
            f'- {command.family_names.str if command.family_names else None}, '
            f'- {command.delivery_place.str}, '
            f'- {command.phone_number.str if command.phone_number else None}, '
            f'- {command.country_phone_code.int if command.country_phone_code else None}'
        )

        client = Client.from_dict(ClientDict(
            client_id=IdValueObject.generate(),
            given_names=command.given_names.str,
            family_names=command.family_names.str if command.family_names else None,
            delivery_place=command.delivery_place.str,
            phone=PhoneDict(
                number=command.phone_number.str,
                country_code=command.country_phone_code.int
            ) if command.phone_number and command.country_phone_code else None,
        ))
        await self._repository.create_client(client)
