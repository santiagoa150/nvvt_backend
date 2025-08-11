from typing import TypedDict

from orders.domain.product.product_dict import ProductDict


class OrderDict(TypedDict):
    """Dictionary representation of an order."""

    order_id: str
    campaign_id: str
    client_id: str
    quantity: int
    status: str
    product: ProductDict
