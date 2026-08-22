from typing import Optional, cast

from motor.motor_asyncio import AsyncIOMotorCollection

from campaigns.domain.campaign import Campaign
from campaigns.domain.campaign_dict import CampaignDict
from campaigns.domain.campaign_status import CampaignStatus
from campaigns.domain.repository.campaign_read_repository import CampaignReadRepository
from campaigns.domain.value_objects.campaign_number import CampaignNumber
from shared.domain.pagination_dict import PaginationDict, empty_pagination_dict
from shared.domain.value_objects.common.year import Year
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.pagination.limit_param import LimitParam
from shared.domain.value_objects.pagination.page_param import PageParam
from shared.infrastructure.mongodb.mongodb_utils import MongoDBUtils

# Ranks statuses so the active campaign surfaces first, then the ones still
# scheduled, then archived ones last.
_STATUS_SORT_WEIGHTS = {
    CampaignStatus.ACTIVE.value: 0,
    CampaignStatus.SCHEDULED.value: 1,
    CampaignStatus.ARCHIVED.value: 2,
}


class MongoDBCampaignReadRepository(CampaignReadRepository):
    """MongoDB implementation of the CampaignReadRepository interface for reading campaign data."""

    def __init__(self, collection: AsyncIOMotorCollection):
        """Initializes the MongoDBCampaignRepository with a MongoDB collection."""
        self._collection = collection

    async def get_campaign_by_id(self, campaign_id: IdValueObject) -> Optional[Campaign]:
        """Retrieves a campaign by its ID from the MongoDB collection."""
        document = await self._collection.find_one({"campaign_id": campaign_id.str})

        if document is None:
            return None

        return Campaign.from_dict(cast(CampaignDict, document))

    async def get_paginated_campaigns(
        self, page: PageParam, limit: LimitParam
    ) -> PaginationDict[Campaign]:
        """Retrieves paginated campaigns from the MongoDB collection."""

        pipeline = [
            {
                "$addFields": {
                    "_status_order": {
                        "$switch": {
                            "branches": [
                                {
                                    "case": {"$eq": ["$status", status_value]},
                                    "then": weight,
                                }
                                for status_value, weight in _STATUS_SORT_WEIGHTS.items()
                            ],
                            "default": len(_STATUS_SORT_WEIGHTS),
                        }
                    }
                }
            },
            *MongoDBUtils.build_paginated_query(
                page, limit, sort={"_status_order": 1, "year": -1, "number": -1}
            ),
        ]
        result = await self._collection.aggregate(pipeline).to_list(length=1)
        aggregated = result[0]

        if not result or not aggregated:
            return empty_pagination_dict()

        # $facet always returns each named facet as an array, even a summary
        # facet with a single document (or none, when the collection is empty).
        metadata_facet = aggregated["metadata"]
        metadata = (
            metadata_facet[0]
            if metadata_facet
            else {"total": 0, "total_pages": 0, "page": page.int}
        )

        campaigns = [Campaign.from_dict(cast(CampaignDict, doc)) for doc in aggregated["data"]]
        return PaginationDict(data=campaigns, metadata=metadata)

    async def exists_by_year_and_number(self, year: Year, number: CampaignNumber) -> bool:
        """Checks if a campaign exists by year and number."""
        document = await self._collection.find_one({"year": year.int, "number": number.int})
        return document is not None

    async def exists_active_campaign(self) -> bool:
        """Checks if there is already an active campaign."""
        document = await self._collection.find_one({"status": CampaignStatus.ACTIVE.value})
        return document is not None
