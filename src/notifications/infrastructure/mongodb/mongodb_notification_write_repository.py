from typing import List

from motor.motor_asyncio import AsyncIOMotorCollection

from notifications.domain.notification import Notification
from notifications.domain.repository.notification_write_repository import (
    NotificationWriteRepository,
)
from shared.domain.value_objects.id_value_object import IdValueObject


class MongoDBNotificationWriteRepository(NotificationWriteRepository):
    """MongoDB implementation of the NotificationWriteRepository interface."""

    def __init__(self, collection: AsyncIOMotorCollection):
        """Initializes the MongoDBNotificationWriteRepository with a MongoDB collection."""
        self._collection = collection

    async def create_notification(self, notification: Notification) -> None:
        """Creates a new notification record in the MongoDB collection."""
        await self._collection.insert_one(notification.to_dict())

    async def mark_as_seen(self, notification_ids: List[IdValueObject]) -> None:
        """Marks the given notifications as seen in the MongoDB collection."""
        await self._collection.update_many(
            {
                "notification_id": {
                    "$in": [notification_id.str for notification_id in notification_ids]
                }
            },
            {"$set": {"seen": True}},
        )
