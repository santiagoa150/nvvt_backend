from enum import Enum


class MongoDBCountryConstants(str, Enum):
    """Constants for MongoDB Countries collection."""

    COLLECTION_NAME = "countries"
