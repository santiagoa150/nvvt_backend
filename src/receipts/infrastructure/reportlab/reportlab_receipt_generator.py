from io import BytesIO
from typing import List

from campaigns.domain.campaign import Campaign
from clients.domain.client import Client
from orders.domain.order import Order
from receipts.domain.repository.receipt_generator import ReceiptGenerator


class ReportlabReceiptGenerator(ReceiptGenerator):
    """Generates receipts using the ReportLab library."""

    async def create_client_receipt(self, campaign: Campaign, client: Client, orders: List[Order]) -> BytesIO:
        pass
