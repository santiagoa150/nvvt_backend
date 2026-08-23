from enum import Enum

from products.domain.exceptions.product_status_exception import ProductStatusException


class ProductStatus(str, Enum):
    """Enumeration of possible product statuses."""

    ACTIVE = "ACTIVE"
    OUT_OF_STOCK = "OUT_OF_STOCK"

    @classmethod
    def create(cls, value: str) -> "ProductStatus":
        if value not in cls._value2member_map_:
            raise ProductStatusException.invalid_product_status(value)
        return cls(value)
