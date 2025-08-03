from abc import ABC, abstractmethod

from campaigns.domain.campaign import Campaign
from shared.domain.value_objects.id_value_object import IdValueObject


class CampaignRepository(ABC):
    """Abstract base class for campaign repository operations."""

    @abstractmethod
    def get_campaign_by_id(self, campaign_id: IdValueObject) -> Campaign | None:
        """Retrieve a campaign by its ID."""
        pass
