import logging
from typing import Awaitable

from notifications.application.query.get.paginated_notifications.get_paginated_notifications_query import (
    GetPaginatedNotificationsQuery,
)
from notifications.domain.notification import Notification
from notifications.domain.repository.notification_read_repository import (
    NotificationReadRepository,
)
from shared.domain.cqrs.query.iquery_handler import IQueryHandler
from shared.domain.pagination_dict import PaginationDict


class GetPaginatedNotificationsQueryHandler(IQueryHandler[GetPaginatedNotificationsQuery]):
    """Handler for the GetPaginatedNotificationsQuery."""

    def __init__(self, repository: NotificationReadRepository):
        """
        :param repository: The notification repository to use for fetching notifications.
        """
        self._repository = repository
        self._logger = logging.getLogger(__name__)

    def handle(
        self, query: GetPaginatedNotificationsQuery
    ) -> Awaitable[PaginationDict[Notification]]:
        """
        Handle the GetPaginatedNotificationsQuery to retrieve a recipient's paginated
        notifications, unseen ones first.

        :param query: The query containing the recipient and pagination parameters.
        :return: A page of the recipient's notifications.
        """
        self._logger.info(
            f"INIT :: Getting notifications for recipient {query.recipient.str} with "
            f"Page: {query.page}, Limit: {query.limit}"
        )
        return self._repository.get_paginated_notifications_by_recipient(
            query.recipient, query.page, query.limit
        )
