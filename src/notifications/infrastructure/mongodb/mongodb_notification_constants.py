from enum import Enum


class MongoDBNotificationConstants(str, Enum):
    """Constants for MongoDB Notifications collection."""

    COLLECTION_NAME = "notifications"
