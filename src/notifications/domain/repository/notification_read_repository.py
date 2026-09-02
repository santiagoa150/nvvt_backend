from abc import ABC, abstractmethod

from notifications.domain.notification import Notification
from shared.domain.pagination_dict import PaginationDict
from shared.domain.value_objects.pagination.limit_param import LimitParam
from shared.domain.value_objects.pagination.page_param import PageParam
from shared.domain.value_objects.str_value_object import StringValueObject


class NotificationReadRepository(ABC):
    """Abstract base class for notification reading repository operations."""

    @abstractmethod
    async def get_paginated_notifications_by_recipient(
        self, recipient: StringValueObject, page: PageParam, limit: LimitParam
    ) -> PaginationDict[Notification]:
        """
        Retrieve paginated notifications for a recipient, unseen ones first.

        :param recipient: The ID of the recipient to retrieve notifications for.
        :param page: The page number to retrieve.
        :param limit: The number of items per page.
        :return: A PaginationDict containing the paginated notifications.
        """
        pass
