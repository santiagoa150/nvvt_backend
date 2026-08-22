from enum import Enum

from campaigns.domain.exceptions.campaign_status_exception import CampaignStatusException


class CampaignStatus(str, Enum):
    """Enumeration of possible campaign statuses."""

    ACTIVE = "ACTIVE"
    SCHEDULED = "SCHEDULED"
    ARCHIVED = "ARCHIVED"

    @classmethod
    def create(cls, value: str) -> "CampaignStatus":
        if value not in cls._value2member_map_:
            raise CampaignStatusException.invalid_campaign_status(value)
        return cls(value)
