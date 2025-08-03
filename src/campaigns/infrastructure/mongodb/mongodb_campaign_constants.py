from enum import Enum


class MongoDBCampaignConstants(str, Enum):
    """Constants for MongoDB Campaigns collection."""
    COLLECTION_NAME = "campaigns"
