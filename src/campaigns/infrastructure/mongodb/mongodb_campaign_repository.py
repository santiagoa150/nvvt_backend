from typing import cast
from motor.motor_asyncio import AsyncIOMotorCollection

from campaigns.domain.campaign import Campaign
from campaigns.domain.campaign_dict import CampaignDict
from campaigns.domain.repository.campaign_repository import CampaignRepository
from shared.domain.pagination_dict import PaginationDict, empty_pagination_dict
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.pagination.limit_param import LimitParam
from shared.domain.value_objects.pagination.page_param import PageParam
from shared.infrastructure.mongodb.mongodb_utils import MongoDBUtils


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

    async def get_paginated_campaigns(self, page: PageParam, limit: LimitParam) -> PaginationDict[Campaign]:
        """Retrieves paginated campaigns from the MongoDB collection."""

        pipeline = MongoDBUtils.build_paginated_query(page, limit)
        result = await self._collection.aggregate(pipeline).to_list(length=1)
        aggregated = result[0]

        if not result or not aggregated:
            return empty_pagination_dict()

        campaigns = [Campaign.from_dict(cast(CampaignDict, doc)) for doc in aggregated['data']]
        return PaginationDict(data=campaigns, metadata=aggregated['metadata'])
