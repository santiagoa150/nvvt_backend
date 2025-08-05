from abc import ABC, abstractmethod
from typing import Optional

from orders.domain.order import Order
from shared.domain.value_objects.id_value_object import IdValueObject


class OrderReadRepository(ABC):
    """Abstract base class for order reading repository operations."""

    @abstractmethod
    async def get_order_by_id(self, order_id: IdValueObject) -> Optional[Order]:
        """
        Retrieve an order by its ID.

        :param order_id: The ID of the order to retrieve.
        :return: An Order object if found, otherwise None.
        """
        pass
