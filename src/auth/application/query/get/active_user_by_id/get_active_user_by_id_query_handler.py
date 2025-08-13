import logging

from auth.application.query import GetActiveUserByIdQuery
from auth.domain.repository.user_read_repository import UserReadRepository
from auth.domain.user import User
from shared.domain.cqrs.query.iquery_handler import IQueryHandler
from shared.domain.exceptions.not_found_exception import NotFoundException


class GetActiveUserByIdQueryHandler(IQueryHandler[GetActiveUserByIdQuery]):
    """Handler for the GetActiveUserByIdQuery."""

    def __init__(self, repository: UserReadRepository):
        """
        :param repository: The user repository to use for fetching users.
        """
        self._repository = repository
        self._logger = logging.getLogger(__name__)

    async def handle(self, query: GetActiveUserByIdQuery):
        """
        Handle the GetActiveUserByIdQuery to retrieve an active user by their ID.

        :param query: The query containing the user's ID.
        :return: The active user associated with the provided ID.
        :raises NotFoundException: If no user is found with the given ID.
        """
        self._logger.info(f"INIT :: User ID: {query.user_id.str}")
        user = await self._repository.get_active_user_by_id(query.user_id)

        if not user:
            raise NotFoundException.entity_not_found(User.__name__, query.user_id.str)

        return user
