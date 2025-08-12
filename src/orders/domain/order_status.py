from enum import Enum

from orders.domain.exceptions.order_status_exception import OrderStatusException


class OrderStatus(str, Enum):
    """Enumeration of possible order statuses."""

    ACTIVE = 'ACTIVE'
    OUT_OF_STOCK = 'OUT_OF_STOCK'

    @classmethod
    def create(cls, value: str) -> "OrderStatus":
        if value not in cls._value2member_map_:
            raise OrderStatusException.invalid_order_status(value)
        return cls(value)
