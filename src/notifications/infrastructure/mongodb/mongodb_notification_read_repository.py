from typing import cast

from motor.motor_asyncio import AsyncIOMotorCollection

from notifications.domain.notification import Notification
from notifications.domain.notification_dict import NotificationDict
from notifications.domain.repository.notification_read_repository import (
    NotificationReadRepository,
)
from shared.domain.pagination_dict import PaginationDict, empty_pagination_dict
from shared.domain.value_objects.pagination.limit_param import LimitParam
from shared.domain.value_objects.pagination.page_param import PageParam
from shared.domain.value_objects.str_value_object import StringValueObject
from shared.infrastructure.mongodb.mongodb_utils import MongoDBUtils

# Unseen notifications (seen=False) sort before seen ones, newest first within each group.
_SORT_UNSEEN_FIRST = {"seen": 1, "_id": -1}


class MongoDBNotificationReadRepository(NotificationReadRepository):
    """MongoDB implementation of the NotificationReadRepository interface."""

    def __init__(self, collection: AsyncIOMotorCollection):
        """Initializes the MongoDBNotificationReadRepository with a MongoDB collection."""
        self._collection = collection

    async def get_paginated_notifications_by_recipient(
        self, recipient: StringValueObject, page: PageParam, limit: LimitParam
    ) -> PaginationDict[Notification]:
        """Retrieves a recipient's paginated notifications, unseen ones first."""
        pipeline = [
            {"$match": {"recipient": recipient.str}},
            *MongoDBUtils.build_paginated_query(page, limit, sort=_SORT_UNSEEN_FIRST),
        ]
        result = await self._collection.aggregate(pipeline).to_list(length=1)
        aggregated = result[0] if result else None

        if not aggregated:
            return empty_pagination_dict()

        # $facet always returns each named facet as an array, even a summary
        # facet with a single document (or none, when the collection is empty).
        metadata_facet = aggregated["metadata"]
        metadata = (
            metadata_facet[0]
            if metadata_facet
            else {"total": 0, "total_pages": 0, "page": page.int}
        )

        notifications = [
            Notification.from_dict(cast(NotificationDict, doc)) for doc in aggregated["data"]
        ]
        return PaginationDict(data=notifications, metadata=metadata)
