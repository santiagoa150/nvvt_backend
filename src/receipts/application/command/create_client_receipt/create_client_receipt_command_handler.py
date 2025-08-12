import logging

from campaigns.application.query.get_campaign_by_id.get_campaign_by_id_query import GetCampaignByIdQuery
from campaigns.domain.campaign import Campaign
from clients.application.query.get_client_by_id.get_client_by_id_query import GetClientByIdQuery
from clients.domain.client import Client
from orders.application.query.get_orders_by_campaign.get_orders_by_campaign_query import GetOrdersByCampaignQuery
from orders.domain.order import Order
from orders.domain.order_status import OrderStatus
from receipts.application.command.create_client_receipt.create_client_receipt_command import CreateClientReceiptCommand, \
    CreateClientReceiptCommandResponse
from receipts.domain.repository.receipt_generator import ReceiptGenerator
from shared.domain.cqrs.command.icommand_handler import ICommandHandler
from shared.domain.cqrs.query.query_bus import QueryBus
from shared.domain.exceptions.not_found_exception import NotFoundException


class CreateClientReceiptCommandHandler(ICommandHandler[CreateClientReceiptCommand]):
    """Handler for the CreateClientReceiptCommand."""

    def __init__(self, query_bus: QueryBus, receipt_generator: ReceiptGenerator):
        """
        :param query_bus: The query bus to use for querying campaigns and clients.
        :param receipt_generator: The receipt generator to use for creating receipts.
        """
        self._query_bus = query_bus
        self._receipt_generator = receipt_generator
        self._logger = logging.getLogger(__name__)

    async def handle(self, command: CreateClientReceiptCommand) -> CreateClientReceiptCommandResponse:
        """
        Handle the CreateClientReceiptCommand to create a new client receipt.
        :param command: The command containing the receipt details.
        """
        self._logger.info(
            f'INIT :: Generating receipt for Campaign and Client :: {command.campaign_id.str}, {command.client_id.str}'
        )
        campaign: Campaign = await self._query_bus.query(GetCampaignByIdQuery(command.campaign_id))
        client: Client = await self._query_bus.query(GetClientByIdQuery(command.client_id))
        orders: dict[str, list[Order]] = await self._query_bus.query(GetOrdersByCampaignQuery(
            command.campaign_id,
            command.client_id,
        ))

        if not orders.get(OrderStatus.ACTIVE.value):
            self._logger.warning(
                f'No active orders found for Campaign ID {command.campaign_id.str} and Client ID {command.client_id.str}'
            )
            raise NotFoundException.entity_not_found(
                Order.__name__, f'ACTIVE ORDERS for client {command.client_id.str}'
            )

        receipt = await self._receipt_generator.create_client_receipt(
            campaign,
            client,
            orders.get(OrderStatus.ACTIVE.value),
            orders.get(OrderStatus.OUT_OF_STOCK.value, None)
        )
        receipt_name = f'Recibo-{client.full_name.str}-Campaña-{campaign.year.int}-{campaign.number.int}.pdf'

        return CreateClientReceiptCommandResponse(
            receipt=receipt,
            title=receipt_name
        )
