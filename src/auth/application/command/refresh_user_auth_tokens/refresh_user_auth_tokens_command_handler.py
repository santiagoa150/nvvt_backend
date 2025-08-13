import logging
from typing import cast

from auth.application.command import RefreshUserAuthTokensCommand
from auth.application.query import GetActiveUserByIdQuery
from auth.domain.auth_data import AuthData
from auth.domain.auth_tokens import AuthTokens
from auth.domain.exceptions.unauthorized_exception import UnauthorizedException
from auth.domain.refresh_data import RefreshData
from auth.domain.repository.token_repository import TokenRepository
from settings import settings
from shared.domain.cqrs.command.icommand_handler import ICommandHandler
from shared.domain.cqrs.query.query_bus import QueryBus


class RefreshUserAuthTokensCommandHandler(ICommandHandler[RefreshUserAuthTokensCommand]):
    """
    Command handler for refreshing user authentication tokens.
    This handler is responsible for processing the refresh token command.
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

    async def handle(self, command: RefreshUserAuthTokensCommand) -> AuthTokens:
        """
        Handle the RefreshUserAuthTokensCommand to refresh user authentication tokens.
        :param command: The command containing the user's refresh token.
        """
        self._logger.info("Refreshing user authentication tokens")

        raw_refresh_data = await self._token_repository.verify(
            command.refresh_token, settings.jwt_refresh_secret
        )

        if not raw_refresh_data:
            raise UnauthorizedException.invalid_refresh_token()

        refresh_data = cast(RefreshData, raw_refresh_data)

        user = await self._query_bus.query(GetActiveUserByIdQuery.create(refresh_data["user_id"]))

        access_token = await self._token_repository.sign(
            dict(AuthData(user_id=user.user_id.str, email=user.email.str)),
            settings.jwt_secret,
            settings.jwt_expires_in,
        )
        refresh_token = await self._token_repository.sign(
            raw_refresh_data, settings.jwt_refresh_secret, settings.jwt_refresh_expires_in
        )

        return AuthTokens(access_token=access_token, refresh_token=refresh_token)
