from typing import cast
from motor.motor_asyncio import AsyncIOMotorCollection

from campaigns.domain.campaign import Campaign
from campaigns.domain.campaign_dict import CampaignDict
from campaigns.domain.repository.campaign_repository import CampaignRepository
from shared.domain.value_objects.id_value_object import IdValueObject


class MongoDBCampaignRepository(CampaignRepository):
    """MongoDB implementation of the CampaignRepository interface."""

    def __init__(self, collection: AsyncIOMotorCollection):
        """Initializes the MongoDBCampaignRepository with a MongoDB collection."""
        self._collection = collection

    async def get_campaign_by_id(self, campaign_id: IdValueObject) -> Campaign | None:
        """Retrieves a campaign by its ID from the MongoDB collection."""
        document = await self._collection.find_one({'campaign_id': campaign_id.str})

        if document is None:
            return None

        return Campaign.from_dict(cast(CampaignDict, document))
