from abc import ABC, abstractmethod

from campaigns.domain.campaign import Campaign
from campaigns.domain.campaign_status import CampaignStatus
from shared.domain.value_objects.id_value_object import IdValueObject


class CampaignWriteRepository(ABC):
    """Abstract base class for campaign writing repository operations."""

    @abstractmethod
    async def create_campaign(self, campaign: Campaign) -> None:
        """
        Create a new campaign.

        :param campaign: The campaign object to create.
        """
        pass

    @abstractmethod
    async def delete_campaign(self, campaign_id: IdValueObject) -> bool:
        """
        Delete an existing campaign.

        :param campaign_id: The ID of the campaign to delete.
        :return: True if the campaign was deleted successfully, False otherwise.
        """
        pass

    @abstractmethod
    async def update_campaign_status(
        self, campaign_id: IdValueObject, status: CampaignStatus
    ) -> None:
        """
        Update the status of an existing campaign.

        :param campaign_id: The ID of the campaign to update.
        :param status: The new status for the campaign.
        """
        pass
