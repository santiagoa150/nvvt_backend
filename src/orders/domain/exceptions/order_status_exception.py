from fastapi import status

from orders.domain.exceptions.order_exception_messages import OrderExceptionMessages
from shared.domain.exceptions.common_exception import CommonException


class OrderStatusException(CommonException):
    """Exception raised when there is an issue with the order status."""

    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code, message)

    @staticmethod
    def invalid_order_status(value: str) -> "OrderStatusException":
        """Raises an exception when the order status is invalid."""
        return OrderStatusException(
            OrderExceptionMessages.INVALID_ORDER_STATUS.format(order_status=value),
        )
