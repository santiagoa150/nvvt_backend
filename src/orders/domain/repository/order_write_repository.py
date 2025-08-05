from abc import ABC, abstractmethod

from orders.domain.order import Order


class OrderWriteRepository(ABC):
    """Abstract base class for order writing repository operations."""

    @abstractmethod
    async def create_order(self, order: Order) -> None:
        """
        Create a new order.

        :param order: The order object to create.
        """
        pass
