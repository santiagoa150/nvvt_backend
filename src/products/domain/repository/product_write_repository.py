from abc import ABC, abstractmethod

from products.domain.product import Product
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.positive_int_value_object import PositiveIntValueObject


class ProductWriteRepository(ABC):
    """Abstract base class for product writing repository operations."""

    @abstractmethod
    async def create_product(self, product: Product) -> None:
        """
        Create a new product.

        :param product: The product to create.
        """
        pass

    @abstractmethod
    async def delete_product(self, product_id: IdValueObject) -> bool:
        """
        Delete an existing product.

        :param product_id: The ID of the product to delete.
        :return: True if the product was deleted successfully, False otherwise.
        """
        pass

    @abstractmethod
    async def update_product_quantity(
        self, product_id: IdValueObject, quantity: PositiveIntValueObject
    ) -> None:
        """
        Update the quantity of an existing product.

        :param product_id: The ID of the product to update.
        :param quantity: The new quantity for the product.
        """
        pass
