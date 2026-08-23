from fastapi import status

from products.domain.exceptions.product_exception_messages import ProductExceptionMessages
from shared.domain.exceptions.common_exception import CommonException


class ProductProviderException(CommonException):
    """Exception raised when there is an issue with the product provider."""

    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        super().__init__(status_code, message)

    @staticmethod
    def cannot_get_product_provider() -> "ProductProviderException":
        """Raises an exception when the product provider cannot be retrieved."""
        return ProductProviderException(ProductExceptionMessages.CANNOT_GET_PRODUCT_PROVIDER.value)

    @staticmethod
    def invalid_product_url(product_url: str) -> "ProductProviderException":
        """Raises an exception when the product URL is invalid."""
        return ProductProviderException(
            ProductExceptionMessages.INVALID_PRODUCT_URL.format(product_url=product_url),
            status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def expired_provider_credentials() -> "ProductProviderException":
        """Raises an exception when the product provider credentials have expired."""
        return ProductProviderException(
            ProductExceptionMessages.PROVIDER_CREDENTIALS_EXPIRED.value, status.HTTP_400_BAD_REQUEST
        )

    @staticmethod
    def cannot_build_product_data() -> "ProductProviderException":
        """Raises an exception when there is an error building product data."""
        return ProductProviderException(ProductExceptionMessages.CANNOT_BUILD_PRODUCT_DATA.value)

    @staticmethod
    def product_not_found_in_provider(product_code: str) -> "ProductProviderException":
        """Raises an exception when the product code doesn't exist in the provider."""
        return ProductProviderException(
            ProductExceptionMessages.PRODUCT_NOT_FOUND_IN_PROVIDER.format(
                product_code=product_code
            ),
            status.HTTP_400_BAD_REQUEST,
        )
