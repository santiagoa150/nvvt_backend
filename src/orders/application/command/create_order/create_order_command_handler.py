import logging

from campaigns.application.query.get_campaign_by_id.get_campaign_by_id_query import GetCampaignByIdQuery
from clients.application.query.get_client_by_id.get_client_by_id_query import GetClientByIdQuery
from orders.application.command.create_order.create_order_command import CreateOrderCommand
from orders.domain.order import Order
from orders.domain.order_dict import OrderDict
from orders.domain.repository.order_client import OrderClient
from orders.domain.repository.order_read_repository import OrderReadRepository
from orders.domain.repository.order_write_repository import OrderWriteRepository
from shared.domain.cqrs.command.icommand_handler import ICommandHandler
from shared.domain.cqrs.query.query_bus import QueryBus
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.positive_int_value_object import PositiveIntValueObject


class CreateOrderCommandHandler(ICommandHandler[CreateOrderCommand]):
    """Handler for the CreateOrderCommand."""

    def __init__(
            self,
            query_bus: QueryBus,
            read_repository: OrderReadRepository,
            write_repository: OrderWriteRepository,
            order_client: OrderClient,
    ):
        """
        :param query_bus: The query bus to use for querying order providers.
        :param read_repository: The repository to use for reading orders.
        :param write_repository: The repository to use for writing orders.
        :param order_client: The repository to use for reading order providers.
        """
        self._query_bus = query_bus
        self._read_repository = read_repository
        self._write_repository = write_repository
        self._order_client = order_client
        self._logger = logging.getLogger(__name__)

    async def handle(self, command: CreateOrderCommand) -> None:
        """
        Handle the CreateOrderCommand to create a new order.
        :param command: The command containing the order details.
        """
        self._logger.info(
            f'INIT :: Validating Campaign and Client :: {command.campaign_id.str}, {command.client_id.str}'
        )
        await self._query_bus.query(GetCampaignByIdQuery(command.campaign_id))
        await self._query_bus.query(GetClientByIdQuery(command.client_id))

        self._logger.info(f'Searching {command.product_url.str} on client')
        product = await self._order_client.build_product(command.provider, command.product_url)

        current_order = await self._read_repository.get_order_by_campaign_client_code(
            command.campaign_id,
            command.client_id,
            product.code
        )

        if current_order:
            self._logger.info(f'Order with product {product.code.str} already exists, updating quantity')
            current_order.quantity = PositiveIntValueObject(current_order.quantity.int + command.quantity.int)
            await self._write_repository.update_order(current_order)

        else:
            self._logger.info(f'Creating order with product {product.code.str} and quantity {command.quantity.int}')
            order = Order.from_dict(OrderDict(
                order_id=IdValueObject.generate(),
                product=product.to_dict(),
                campaign_id=command.campaign_id.str,
                client_id=command.client_id.str,
                quantity=command.quantity.int,
                status=command.status.value
            ))

            await self._write_repository.create_order(order)
