from enum import Enum


class CampaignExceptionMessages(str, Enum):
    """Exception messages related to campaigns."""

    YEAR_AND_NUMBER_ALREADY_EXISTS = "Campaign with year {year} and number {number} already exists."
    ACTIVE_CAMPAIGN_ALREADY_EXISTS = "An active campaign already exists."

    def format(self, **kwargs) -> str:
        return self.value.format(**kwargs)
