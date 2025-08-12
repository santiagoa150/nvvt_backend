import logging

from auth.application.command.create_user.create_user_command import CreateUserCommand
from auth.domain.exceptions.user_already_exists_exception import UserAlreadyExistsException
from auth.domain.repository.user_read_repository import UserReadRepository
from auth.domain.repository.user_write_repository import UserWriteRepository
from auth.domain.user import User
from auth.domain.user_dict import UserDict
from auth.domain.value_objects.password_hash import PasswordHash
from shared.domain.cqrs.command.icommand_handler import ICommandHandler, Command
from shared.domain.value_objects.id_value_object import IdValueObject


class CreateUserCommandHandler(ICommandHandler[CreateUserCommand]):

    def __init__(
            self,
            read_repository: UserReadRepository,
            write_repository: UserWriteRepository,
    ):
        """
        :param read_repository: The user repository to use for reading users.
        :param write_repository: The user repository to use for writing users.
        """
        self._read_repository = read_repository
        self._write_repository = write_repository
        self._logger = logging.getLogger(__name__)

    async def handle(self, command: CreateUserCommand) -> None:
        self._logger.info(f'INIT :: Creating User with params: {command.email.str}')

        if await self._read_repository.get_user_by_email(command.email):
            raise UserAlreadyExistsException.email_already_exists(command.email.str)

        password_hash = PasswordHash.create_from(command.password)

        user = User.from_dict(UserDict(
            user_id=IdValueObject.generate(),
            email=command.email.str,
            password=password_hash.str,
            is_active=True,
        ))

        await self._write_repository.create_user(user)
