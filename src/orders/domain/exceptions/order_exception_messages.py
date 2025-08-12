from enum import Enum


class OrderExceptionMessages(str, Enum):
    """Class containing exception messages for order domain exceptions."""

    CANNOT_GET_PRODUCT_PROVIDER = "Cannot get product provider."
    INVALID_PRODUCT_URL = "Invalid product URL: {product_url}"
    PROVIDER_CREDENTIALS_EXPIRED = "Order provider credentials have expired."
    CANNOT_BUILD_PRODUCT_DATA = "Error building product data from provider."
    INVALID_ORDER_STATUS = "Invalid order status: {order_status}"

    def format(self, **kwargs) -> str:
        """Format the message with the provided keyword arguments."""
        return self.value.format(**kwargs)
