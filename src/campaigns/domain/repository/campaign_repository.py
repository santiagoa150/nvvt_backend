from abc import ABC, abstractmethod
from typing import Optional

from campaigns.domain.campaign import Campaign
from shared.domain.value_objects.id_value_object import IdValueObject


class CampaignRepository(ABC):
    """Abstract base class for campaign repository operations."""

    @abstractmethod
    async def get_campaign_by_id(self, campaign_id: IdValueObject) -> Optional[Campaign]:
        """Retrieve a campaign by its ID."""
        pass
