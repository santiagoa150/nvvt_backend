from abc import ABC, abstractmethod
from io import BytesIO
from typing import Dict, List, Optional

from campaigns.domain.campaign import Campaign
from clients.domain.client import Client
from orders.domain.order import Order
from products.domain.product import Product


class ReceiptGenerator(ABC):
    """Abstract base class for generating receipts."""

    @abstractmethod
    async def create_client_receipt(
        self,
        campaign: Campaign,
        client: Client,
        active_orders: List[Order],
        out_of_stock_orders: Optional[List[Order]],
        products_by_id: Dict[str, Product],
    ) -> BytesIO:
        """
        Create a receipt for a client based on the campaign and orders.

        :param campaign: The campaign associated with the receipt.
        :param client: The client for whom the receipt is created.
        :param active_orders: The list of active orders associated with the receipt.
        :param out_of_stock_orders: Optional orders that were out of stock.
        :param products_by_id: The products referenced by the orders, keyed by product_id.
        :return: A BytesIO object containing the generated receipt.
        """
        pass
