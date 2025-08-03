from motor.motor_asyncio import AsyncIOMotorCollection

from campaigns.domain.campaign import Campaign
from campaigns.domain.repository.campaign_write_repository import CampaignWriteRepository


class MongoDBCampaignWriteRepository(CampaignWriteRepository):
    """MongoDB implementation of the CampaignWriteRepository for writing campaign data."""

    def __init__(self, collection: AsyncIOMotorCollection):
        """Initializes the MongoDBCampaignRepository with a MongoDB collection."""
        self._collection = collection

    async def create_campaign(self, campaign: Campaign) -> None:
        """Creates a new campaign in the MongoDB collection."""
        await self._collection.insert_one(campaign.to_dict())
