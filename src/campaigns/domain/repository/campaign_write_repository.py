from abc import ABC, abstractmethod

from campaigns.domain.campaign import Campaign
from shared.domain.value_objects.id_value_object import IdValueObject


class CampaignWriteRepository(ABC):
    """Abstract base class for campaign writing repository operations."""

    @abstractmethod
    async def create_campaign(self, campaign: Campaign) -> None:
        """Create a new campaign."""
        pass

    @abstractmethod
    async def delete_campaign(self, campaign_id: IdValueObject) -> bool:
        """
        Delete an existing campaign.
        :return: True if the campaign was deleted successfully, False otherwise.
        """
        pass
