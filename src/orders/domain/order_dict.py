from typing import TypedDict


class OrderDict(TypedDict):
    """Dictionary representation of an order."""

    order_id: str
    client_id: str
    client_quantity: int
    product_id: str
