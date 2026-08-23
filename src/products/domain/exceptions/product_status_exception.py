from fastapi import status

from products.domain.exceptions.product_exception_messages import ProductExceptionMessages
from shared.domain.exceptions.common_exception import CommonException


class ProductStatusException(CommonException):
    """Exception raised when there is an issue with the product status."""

    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code, message)

    @staticmethod
    def invalid_product_status(value: str) -> "ProductStatusException":
        """Raises an exception when the product status is invalid."""
        return ProductStatusException(
            ProductExceptionMessages.INVALID_PRODUCT_STATUS.format(product_status=value),
        )
