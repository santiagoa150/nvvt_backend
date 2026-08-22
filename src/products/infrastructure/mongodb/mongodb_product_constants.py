from enum import Enum


class MongoDBProductConstants(str, Enum):
    """Constants for MongoDB Products collection."""

    COLLECTION_NAME = "products"
