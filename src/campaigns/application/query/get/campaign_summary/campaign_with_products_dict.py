from typing import List, TypedDict

from campaigns.domain.campaign_summary_dict import CampaignSummaryDict
from products.domain.product_dict import ProductDict


class CampaignWithProductsDict(TypedDict):
    """Dictionary representation of a campaign, its products, and their pricing summary."""

    campaign_id: str
    name: str
    year: int
    number: int
    status: str
    products: List[ProductDict]
    summary: CampaignSummaryDict
