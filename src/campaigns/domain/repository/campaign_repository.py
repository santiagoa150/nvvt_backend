from abc import ABC, abstractmethod
from typing import Optional

from campaigns.domain.campaign import Campaign
from shared.domain.pagination_dict import PaginationDict
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.pagination.limit_param import LimitParam
from shared.domain.value_objects.pagination.page_param import PageParam


class CampaignRepository(ABC):
    """Abstract base class for campaign repository operations."""

    @abstractmethod
    async def get_campaign_by_id(self, campaign_id: IdValueObject) -> Optional[Campaign]:
        """Retrieve a campaign by its ID."""
        pass

    @abstractmethod
    async def get_paginated_campaigns(self, page: PageParam, limit: LimitParam) -> PaginationDict[Campaign]:
        """Retrieve paginated campaigns."""
        pass
