import logging
from typing import Optional, cast

from auth.application.query.verify_user_access_token.verify_user_access_token_query import (
    VerifyUserAccessTokenQuery,
)
from auth.domain.auth_data import AuthData
from auth.domain.repository.token_repository import TokenRepository
from settings import settings
from shared.domain.cqrs.query.iquery_handler import IQueryHandler


class VerifyUserAccessTokenQueryHandler(IQueryHandler[VerifyUserAccessTokenQuery]):
    """Handler for the VerifyUserAccessTokenQuery."""

    def __init__(self, repository: TokenRepository):
        """
        :param repository: The token repository to use for verifying access tokens.
        """
        self._repository = repository
        self._logger = logging.getLogger(__name__)

    async def handle(self, query: VerifyUserAccessTokenQuery) -> Optional[AuthData]:
        """
        Handle the VerifyUserAccessTokenQuery to verify a user's access token.

        :param query: The query containing the access token.
        :return: True if the access token is valid, False otherwise.
        """
        self._logger.info(f"INIT :: Verifying access token")
        auth_data = await self._repository.verify(query.access_token, settings.jwt_secret)

        if not auth_data:
            return None

        return cast(AuthData, auth_data)
