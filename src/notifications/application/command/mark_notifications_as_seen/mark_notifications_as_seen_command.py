from typing import List

from shared.domain.cqrs.command.icommand import ICommand
from shared.domain.value_objects.id_value_object import IdValueObject


class MarkNotificationsAsSeenCommand(ICommand):
    """Command to mark a list of notifications as seen."""

    def __init__(self, notification_ids: List[IdValueObject]):
        """
        :param notification_ids: The IDs of the notifications to mark as seen.
        """
        self.notification_ids = notification_ids

    @staticmethod
    def create(notification_ids: List[str]) -> "MarkNotificationsAsSeenCommand":
        """Factory method to create a MarkNotificationsAsSeenCommand instance."""
        return MarkNotificationsAsSeenCommand(
            notification_ids=[
                IdValueObject(notification_id, "notification_id")
                for notification_id in notification_ids
            ]
        )
