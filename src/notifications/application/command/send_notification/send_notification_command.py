from notifications.domain.notification import Notification
from shared.domain.cqrs.command.icommand import ICommand
from shared.domain.value_objects.str_value_object import StringValueObject


class SendNotificationCommand(ICommand):
    """Command to send a notification to a recipient."""

    def __init__(self, notification: Notification):
        """
        :param notification: The notification to send.
        """
        self.notification = notification

    @staticmethod
    def create(action: str, recipient: str) -> "SendNotificationCommand":
        """Factory method to create a SendNotificationCommand instance."""
        return SendNotificationCommand(
            notification=Notification(
                action=StringValueObject(action, "notification_action"),
                recipient=StringValueObject(recipient, "notification_recipient"),
            )
        )
