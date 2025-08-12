from fastapi import status

from orders.domain.exceptions.order_exception_messages import OrderExceptionMessages
from shared.domain.exceptions.common_exception import CommonException


class ProductProviderException(CommonException):
    """Exception raised when there is an issue with the order provider."""

    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        super().__init__(status_code, message)

    @staticmethod
    def cannot_get_product_provider() -> "ProductProviderException":
        """Raises an exception when the order provider cannot be retrieved."""
        return ProductProviderException(
            OrderExceptionMessages.CANNOT_GET_PRODUCT_PROVIDER.value
        )

    @staticmethod
    def invalid_product_url(product_url: str) -> "ProductProviderException":
        """Raises an exception when the product URL is invalid."""
        return ProductProviderException(
            OrderExceptionMessages.INVALID_PRODUCT_URL.format(product_url=product_url),
            status.HTTP_400_BAD_REQUEST
        )

    @staticmethod
    def expired_provider_credentials() -> "ProductProviderException":
        """Raises an exception when the order provider credentials have expired."""
        return ProductProviderException(
            OrderExceptionMessages.PROVIDER_CREDENTIALS_EXPIRED.value,
            status.HTTP_400_BAD_REQUEST
        )

    @staticmethod
    def cannot_build_product_data() -> "ProductProviderException":
        """Raises an exception when there is an error building product data."""
        return ProductProviderException(
            OrderExceptionMessages.CANNOT_BUILD_PRODUCT_DATA.value
        )
