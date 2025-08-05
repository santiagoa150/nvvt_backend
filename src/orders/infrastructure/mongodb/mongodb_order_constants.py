from enum import Enum


class MongoDBOrderConstants(str, Enum):
    """Constants for MongoDB Orders collection."""
    COLLECTION_NAME = "orders"
