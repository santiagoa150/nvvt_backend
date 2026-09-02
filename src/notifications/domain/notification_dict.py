from typing import Optional, TypedDict


class NotificationDict(TypedDict):
    """Dictionary representation of a notification."""

    notification_id: str
    action: str
    recipient: str
    seen: bool
    reference: Optional[str]
