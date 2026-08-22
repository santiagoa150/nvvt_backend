from typing import TypedDict


class OrderDict(TypedDict):
    """Dictionary representation of an order."""

    order_id: str
    client_id: str
    quantity: int
    status: str
    product_id: str
