from enum import Enum


class ProductExceptionMessages(str, Enum):
    """Class containing exception messages for product domain exceptions."""

    CANNOT_GET_PRODUCT_PROVIDER = "Cannot get product provider."
    INVALID_PRODUCT_URL = "Invalid product URL: {product_url}"
    PROVIDER_CREDENTIALS_EXPIRED = "Product provider credentials have expired."
    CANNOT_BUILD_PRODUCT_DATA = "Error building product data from provider."
    INVALID_PRODUCT_STATUS = "Invalid product status: {product_status}"
    INVALID_INSTALLMENT_AMOUNTS_SIZE = (
        "installment_amounts must contain exactly {installments} entry(ies) to match "
        "installments, but got {actual}."
    )
    PRODUCT_NOT_FOUND_IN_PROVIDER = (
        "Product with code {product_code} was not found in the provider."
    )
    PRODUCT_ALREADY_EXISTS = (
        "Product with code {product_code} already exists for campaign {campaign_id}."
    )
    CAMPAIGN_NOT_ACTIVE = "Campaign {campaign_id} must be active to create products for it."
    CAMPAIGN_NOT_ACTIVE_TO_DELETE_PRODUCT = (
        "Campaign {campaign_id} must be active to delete its products."
    )

    def format(self, **kwargs) -> str:
        """Format the message with the provided keyword arguments."""
        return self.value.format(**kwargs)
