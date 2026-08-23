from abc import ABC, abstractmethod

from products.domain.product import Product


class ProductWriteRepository(ABC):
    """Abstract base class for product writing repository operations."""

    @abstractmethod
    async def create_product(self, product: Product) -> None:
        """
        Create a new product.

        :param product: The product to create.
        """
        pass
