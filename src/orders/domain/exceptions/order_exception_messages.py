from enum import Enum


class OrderExceptionMessages(str, Enum):
    """Class containing exception messages for order domain exceptions."""

    INVALID_ORDER_STATUS = "Invalid order status: {order_status}"

    def format(self, **kwargs) -> str:
        """Format the message with the provided keyword arguments."""
        return self.value.format(**kwargs)
