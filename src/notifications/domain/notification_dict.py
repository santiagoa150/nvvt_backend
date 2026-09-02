from typing import TypedDict


class NotificationDict(TypedDict):
    """Dictionary representation of a notification."""

    action: str
    recipient: str
