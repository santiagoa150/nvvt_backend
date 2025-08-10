from abc import ABC, abstractmethod
from io import BytesIO
from typing import List

from campaigns.domain.campaign import Campaign
from clients.domain.client import Client
from orders.domain.order import Order


class ReceiptGenerator(ABC):
    """Abstract base class for generating receipts."""

    @abstractmethod
    async def create_client_receipt(
            self,
            campaign: Campaign,
            client: Client,
            orders: List[Order]
    ) -> BytesIO:
        """
        Create a receipt for a client based on the campaign and orders.

        :param campaign: The campaign associated with the receipt.
        :param client: The client for whom the receipt is created.
        :param orders: The list of orders associated with the receipt.
        :return: A BytesIO object containing the generated receipt.
        """
        pass
