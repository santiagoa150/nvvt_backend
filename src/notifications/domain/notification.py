from notifications.domain.notification_dict import NotificationDict
from shared.domain.value_objects.str_value_object import StringValueObject


class Notification:
    """Represents a notification, identified by an action and a recipient."""

    __slots__ = ("_action", "_recipient")

    def __init__(self, action: StringValueObject, recipient: StringValueObject):
        self._action = action
        self._recipient = recipient

    @property
    def action(self) -> StringValueObject:
        return self._action

    @property
    def recipient(self) -> StringValueObject:
        return self._recipient

    def to_dict(self) -> NotificationDict:
        """Converts the notification to a dictionary representation."""
        return NotificationDict(action=self._action.str, recipient=self._recipient.str)
