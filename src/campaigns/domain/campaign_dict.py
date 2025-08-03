from typing import TypedDict


class CampaignDict(TypedDict):
    """Dictionary representation of a campaign."""

    campaign_id: str
    name: str
    year: int
    number: int
