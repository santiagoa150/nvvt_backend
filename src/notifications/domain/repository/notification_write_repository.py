from abc import ABC, abstractmethod
from typing import List

from notifications.domain.notification import Notification
from shared.domain.value_objects.id_value_object import IdValueObject


class NotificationWriteRepository(ABC):
    """Abstract base class for notification writing repository operations."""

    @abstractmethod
    async def create_notification(self, notification: Notification) -> None:
        """
        Create a new notification record.

        :param notification: The notification to create.
        """
        pass

    @abstractmethod
    async def mark_as_seen(self, notification_ids: List[IdValueObject]) -> None:
        """
        Mark the given notifications as seen.

        :param notification_ids: The IDs of the notifications to mark as seen.
        """
        pass
