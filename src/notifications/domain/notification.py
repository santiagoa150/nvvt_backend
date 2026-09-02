from notifications.domain.notification_dict import NotificationDict
from shared.domain.value_objects.bool_value_object import BoolValueObject
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.str_value_object import StringValueObject


class Notification:
    """Represents a notification, identified by an action and a recipient."""

    __slots__ = ("_notification_id", "_action", "_recipient", "_seen")

    def __init__(
        self,
        notification_id: IdValueObject,
        action: StringValueObject,
        recipient: StringValueObject,
        seen: BoolValueObject,
    ):
        self._notification_id = notification_id
        self._action = action
        self._recipient = recipient
        self._seen = seen

    @property
    def notification_id(self) -> IdValueObject:
        return self._notification_id

    @property
    def action(self) -> StringValueObject:
        return self._action

    @property
    def recipient(self) -> StringValueObject:
        return self._recipient

    @property
    def seen(self) -> BoolValueObject:
        return self._seen

    def to_dict(self) -> NotificationDict:
        """Converts the notification to a dictionary representation."""
        return NotificationDict(
            notification_id=self._notification_id.str,
            action=self._action.str,
            recipient=self._recipient.str,
            seen=self._seen.bool,
        )

    @classmethod
    def from_dict(cls, notification_dict: NotificationDict) -> "Notification":
        """Creates a Notification instance from a dictionary representation."""
        return cls(
            notification_id=IdValueObject(notification_dict["notification_id"], "notification_id"),
            action=StringValueObject(notification_dict["action"], "notification_action"),
            recipient=StringValueObject(notification_dict["recipient"], "notification_recipient"),
            seen=BoolValueObject(notification_dict["seen"], "notification_seen"),
        )
