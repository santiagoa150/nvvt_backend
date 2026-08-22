import logging

from campaigns.application.query import GetCampaignByIdQuery
from campaigns.domain.campaign import Campaign
from clients.application.query import GetClientByIdQuery
from clients.domain.client import Client
from orders.application.query import GetOrdersByCampaignQuery
from orders.domain.order import Order
from orders.domain.order_status import OrderStatus
from products.application.query import GetProductsByIdsQuery
from receipts.application.command import (
    CreateClientReceiptCommand,
    CreateClientReceiptCommandResponse,
)
from receipts.domain.repository.receipt_generator import ReceiptGenerator
from shared.domain.cqrs.command.icommand_handler import ICommandHandler
from shared.domain.cqrs.query.query_bus import QueryBus
from shared.domain.exceptions.not_found_exception import NotFoundException


class CreateClientReceiptCommandHandler(ICommandHandler[CreateClientReceiptCommand]):
    """Handler for the CreateClientReceiptCommand."""

    def __init__(self, query_bus: QueryBus, receipt_generator: ReceiptGenerator):
        """
        :param query_bus: The query bus to use for querying campaigns, clients, orders and products.
        :param receipt_generator: The receipt generator to use for creating receipts.
        """
        self._query_bus = query_bus
        self._receipt_generator = receipt_generator
        self._logger = logging.getLogger(__name__)

    async def handle(
        self, command: CreateClientReceiptCommand
    ) -> CreateClientReceiptCommandResponse:
        """
        Handle the CreateClientReceiptCommand to create a new client receipt.
        :param command: The command containing the receipt details.
        """
        self._logger.info(
            f"INIT :: Generating receipt for Campaign and Client :: "
            f"{command.campaign_id.str}, {command.client_id.str}"
        )
        campaign: Campaign = await self._query_bus.query(GetCampaignByIdQuery(command.campaign_id))
        client: Client = await self._query_bus.query(GetClientByIdQuery(command.client_id))
        orders: dict[str, list[Order]] = await self._query_bus.query(
            GetOrdersByCampaignQuery(
                command.campaign_id,
                command.client_id,
            )
        )

        active_orders = orders.get(OrderStatus.ACTIVE.value)

        if not active_orders:
            self._logger.warning(
                f"No active orders found for:"
                f"Campaign ID {command.campaign_id.str} and Client ID {command.client_id.str}"
            )
            raise NotFoundException.entity_not_found(
                Order.__name__, f"ACTIVE ORDERS for client {command.client_id.str}"
            )

        out_of_stock_orders = orders.get(OrderStatus.OUT_OF_STOCK.value, None)

        product_ids = [order.product_id for order in active_orders + (out_of_stock_orders or [])]
        products = await self._query_bus.query(GetProductsByIdsQuery(product_ids))
        products_by_id = {product.product_id.str: product for product in products}

        receipt = await self._receipt_generator.create_client_receipt(
            campaign,
            client,
            active_orders,
            out_of_stock_orders,
            products_by_id,
        )
        receipt_name = (
            f"Recibo-{client.full_name.str}-Campaña-{campaign.year.int}-{campaign.number.int}.pdf"
        )

        return CreateClientReceiptCommandResponse(receipt=receipt, title=receipt_name)
