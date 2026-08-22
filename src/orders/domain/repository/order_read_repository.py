from abc import ABC, abstractmethod
from typing import List, Optional

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
    async def get_order_by_client_and_product(
        self, client_id: IdValueObject, product_id: IdValueObject
    ) -> Optional[Order]:
        """
        Retrieve the order a client placed for a specific product.

        :param client_id: The ID of the client associated with the order.
        :param product_id: The ID of the product associated with the order.
        :return: An Order object if found, otherwise None.
        """
        pass

    @abstractmethod
    async def get_orders_by_product_ids(
        self, product_ids: List[IdValueObject], client_id: Optional[IdValueObject]
    ) -> dict[str, list[Order]]:
        """
        Retrieve all orders placed for the given products.

        :param product_ids: The IDs of the products to retrieve orders for.
        :param client_id: Optional client ID to filter orders.
        :return: A dictionary grouping orders by their status.
        """
        pass
