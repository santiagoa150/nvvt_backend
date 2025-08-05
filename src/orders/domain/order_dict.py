from typing import TypedDict


class OrderDict(TypedDict):
    """Dictionary representation of an order."""

    order_id: str
    campaign_id: str
    client_id: str
    code: str
    name: str
    image_url: str
    quantity: int
    catalog_price: float
    list_price: float
