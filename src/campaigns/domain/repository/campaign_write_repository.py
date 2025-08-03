from abc import ABC, abstractmethod

from campaigns.domain.campaign import Campaign


class CampaignWriteRepository(ABC):
    """Abstract base class for campaign writing repository operations."""

    @abstractmethod
    async def create_campaign(self, campaign: Campaign) -> None:
        """Create a new campaign."""
        pass
