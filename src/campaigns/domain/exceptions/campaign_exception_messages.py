from enum import Enum


class CampaignExceptionMessages(str, Enum):
    """Exception messages related to campaigns."""

    YEAR_AND_NUMBER_ALREADY_EXISTS = "Campaign with year {year} and number {number} already exists."
    ACTIVE_CAMPAIGN_ALREADY_EXISTS = "An active campaign already exists."
    INVALID_CAMPAIGN_STATUS = "Invalid campaign status: {campaign_status}"
    CAMPAIGN_CANNOT_BE_DELETED = (
        "Campaign with status {campaign_status} cannot be deleted. "
        "Only campaigns with status SCHEDULED can be deleted."
    )
    CAMPAIGN_ALREADY_ACTIVE = "Campaign {campaign_id} is already active."
    CAMPAIGN_CANNOT_BE_FINISHED = (
        "Campaign with status {campaign_status} cannot be finished. "
        "Only campaigns with status ACTIVE can be finished."
    )

    def format(self, **kwargs) -> str:
        return self.value.format(**kwargs)
