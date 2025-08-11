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

    @abstractmethod
    async def get_orders_by_campaign(
            self,
            campaign_id: IdValueObject,
            client_id: Optional[IdValueObject]
    ) -> dict[str, list[Order]]:
        """
        Retrieve all orders associated with a specific campaign ID.

        :param campaign_id: The ID of the campaign to retrieve orders for.
        :param client_id: Optional client ID to filter orders.
        :return: A dictionary grouping orders by their state.
        """
        pass
