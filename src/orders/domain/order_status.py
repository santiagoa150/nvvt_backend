from enum import Enum


class OrderStatus(str, Enum):
    """Enumeration of possible order statuses."""

    ACTIVE = 'ACTIVE'
    OUT_OF_STOCK = 'OUT_OF_STOCK'
