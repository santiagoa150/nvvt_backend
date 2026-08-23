from typing import TypedDict


class CampaignSummaryDict(TypedDict):
    """Dictionary representation of a campaign's aggregated pricing summary."""

    total_catalog_price: float
    total_list_price: float
    profit: float
