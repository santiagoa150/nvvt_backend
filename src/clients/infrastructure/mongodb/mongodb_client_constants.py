from enum import Enum


class MongoDBClientConstants(str, Enum):
    """Constants for MongoDB Clients collection."""

    COLLECTION_NAME = "clients"
