import logging

from auth.application.query import GetActiveUserByEmailQuery
from auth.domain.repository.user_read_repository import UserReadRepository
from auth.domain.user import User
from shared.domain.cqrs.query.iquery_handler import IQueryHandler
from shared.domain.exceptions.not_found_exception import NotFoundException


class GetActiveUserByEmailQueryHandler(IQueryHandler[GetActiveUserByEmailQuery]):
    """Handler for the GetActiveUserByEmailQuery."""

    def __init__(self, repository: UserReadRepository):
        """
        :param repository: The user repository to use for fetching users.
        """
        self._repository = repository
        self._logger = logging.getLogger(__name__)

    async def handle(self, query: GetActiveUserByEmailQuery) -> User:
        """
        Handle the GetActiveUserByEmailQuery to retrieve an active user by their email.

        :param query: The query containing the user's email.
        :return: The active user associated with the provided email.
        """
        self._logger.info(f"INIT :: Email: {query.email.str}")
        user = await self._repository.get_active_user_by_email(query.email)

        if not user:
            raise NotFoundException.entity_not_found(User.__name__, query.email.str)

        return user
