from typing import Optional

from products.domain.product_provider_dict import ProductProviderDict
from shared.domain.value_objects.str_value_object import StringValueObject


class ProductProvider:
    """Represents the credentials needed to fetch a product from an external provider."""

    __slots__ = ("_provider_token", "_cart_id")

    def __init__(
        self,
        provider_token: StringValueObject,
        cart_id: Optional[StringValueObject],
    ):
        self._provider_token = provider_token
        self._cart_id = cart_id

    @property
    def provider_token(self) -> StringValueObject:
        return self._provider_token

    @property
    def cart_id(self) -> Optional[StringValueObject]:
        return self._cart_id

    def to_dict(self) -> ProductProviderDict:
        """Converts the product provider to a dictionary representation."""
        return ProductProviderDict(
            provider_token=self._provider_token.str,
            cart_id=self._cart_id.str if self._cart_id else None,
        )

    @classmethod
    def from_dict(cls, product_provider_dict: ProductProviderDict) -> "ProductProvider":
        """Creates a ProductProvider instance from a dictionary representation."""
        return cls(
            provider_token=StringValueObject(
                product_provider_dict["provider_token"], "provider_token"
            ),
            cart_id=(
                StringValueObject(product_provider_dict["cart_id"], "cart_id")
                if product_provider_dict.get("cart_id")
                else None
            ),
        )
