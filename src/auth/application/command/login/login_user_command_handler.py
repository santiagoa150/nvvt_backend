import logging

from auth.domain.auth_tokens import AuthTokens
from auth.domain.exceptions.unauthorized_exception import UnauthorizedException
from auth.domain.refresh_data import RefreshData
from settings import settings

from auth.application.command.login.login_user_command import LoginUserCommand
from auth.application.query.get_active_user_by_email.get_active_user_by_email_query import GetActiveUserByEmailQuery
from auth.domain.auth_data import AuthData
from auth.domain.repository.token_repository import TokenRepository
from auth.domain.user import User
from auth.domain.value_objects.password import Password
from shared.domain.cqrs.command.icommand_handler import ICommandHandler
from shared.domain.cqrs.query.query_bus import QueryBus


class LoginUserCommandHandler(ICommandHandler[LoginUserCommand]):
    """
    Command handler for logging in a user.
    This handler is responsible for processing the login command.
    """

    def __init__(
            self,
            query_bus: QueryBus,
            token_repository: TokenRepository,
    ):
        """
        :param query_bus: The query bus to use for querying user information.
        :param token_repository: The token repository to use for managing tokens.
        """
        self._query_bus = query_bus
        self._token_repository = token_repository
        self._logger = logging.getLogger(__name__)

    async def handle(self, command: LoginUserCommand) -> AuthTokens:
        """
        Handle the LoginUserCommand to log in a user.
        :param command: The command containing the user's email and password.
        """
        self._logger.info('Handling LoginUserCommand for email: %s', command.email)

        try:
            password = Password(command.password)

            user: User = await self._query_bus.query(GetActiveUserByEmailQuery.create(command.email))

            if not user.password.compare(password):
                raise UnauthorizedException.user_not_authenticated()

            access_token = await self._token_repository.sign(
                dict(AuthData(
                    user_id=user.user_id.str,
                    email=user.email.str,
                )),
                settings.jwt_secret,
                settings.jwt_expires_in
            )

            refresh_token = await self._token_repository.sign(
                dict(RefreshData(user_id=user.user_id.str)),
                settings.jwt_refresh_secret,
                settings.jwt_refresh_expires_in
            )
            return AuthTokens(access_token=access_token, refresh_token=refresh_token)

        except:
            raise UnauthorizedException.user_not_authenticated()
