from typing import TypedDict


class ProductDict(TypedDict):
    """Dictionary representation of a product."""

    product_id: str
    campaign_id: str
    code: str
    name: str
    image_url: str
    catalog_price: float
    list_price: float
