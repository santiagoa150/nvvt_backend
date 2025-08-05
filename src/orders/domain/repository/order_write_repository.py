from abc import ABC, abstractmethod

from orders.domain.order import Order
from shared.domain.value_objects.id_value_object import IdValueObject


class OrderWriteRepository(ABC):
    """Abstract base class for order writing repository operations."""

    @abstractmethod
    async def create_order(self, order: Order) -> None:
        """
        Create a new order.

        :param order: The order object to create.
        """
        pass

    @abstractmethod
    async def delete_order(self, order_id: IdValueObject) -> bool:
        """
        Delete an existing order.

        :param order_id: The ID of the order to delete.
        :return: True if the order was deleted successfully, False otherwise.
        """
        pass

    @abstractmethod
    async def update_order(self, order: Order) -> None:
        """
        Update an existing order.

        :param order: The order object with updated information.
        """
        pass
