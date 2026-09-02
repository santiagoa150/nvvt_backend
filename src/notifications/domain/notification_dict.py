from typing import TypedDict


class NotificationDict(TypedDict):
    """Dictionary representation of a notification."""

    notification_id: str
    action: str
    recipient: str
    seen: bool
