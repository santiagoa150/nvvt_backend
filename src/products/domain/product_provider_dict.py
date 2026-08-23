from typing import Optional, TypedDict


class ProductProviderDict(TypedDict):
    """Dictionary representation of a product provider."""

    provider_token: str
    cart_id: Optional[str]
