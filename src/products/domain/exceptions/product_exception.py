from fastapi import status

from products.domain.exceptions.product_exception_messages import ProductExceptionMessages
from shared.domain.exceptions.common_exception import CommonException


class ProductException(CommonException):
    """Exception raised when a product's invariants are violated."""

    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code, message)

    @staticmethod
    def invalid_installment_amounts_size(installments: int, actual: int) -> "ProductException":
        """Raises an exception when installment_amounts doesn't have one entry per installment."""
        return ProductException(
            ProductExceptionMessages.INVALID_INSTALLMENT_AMOUNTS_SIZE.format(
                installments=installments, actual=actual
            ),
        )

    @staticmethod
    def campaign_not_active(campaign_id: str) -> "ProductException":
        """Raises an exception when trying to create a product for a non-active campaign."""
        return ProductException(
            ProductExceptionMessages.CAMPAIGN_NOT_ACTIVE.format(campaign_id=campaign_id),
        )
