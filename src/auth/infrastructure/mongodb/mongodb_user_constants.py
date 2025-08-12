from enum import Enum


class MongoDBUserConstants(str, Enum):
    """Constants for MongoDB Users collection."""

    COLLECTION_NAME = "users"
