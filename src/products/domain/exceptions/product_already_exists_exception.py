from fastapi import status

from products.domain.exceptions.product_exception_messages import ProductExceptionMessages
from shared.domain.exceptions.common_exception import CommonException


class ProductAlreadyExistsException(CommonException):
    """Exception raised when a product already exists for a campaign."""

    def __init__(self, message: str):
        super().__init__(status.HTTP_409_CONFLICT, message)

    @staticmethod
    def already_exists_for_campaign(
        campaign_id: str, product_code: str
    ) -> "ProductAlreadyExistsException":
        """Raises an exception when a product with the same code already exists in the campaign."""
        return ProductAlreadyExistsException(
            ProductExceptionMessages.PRODUCT_ALREADY_EXISTS.format(
                product_code=product_code, campaign_id=campaign_id
            ),
        )
