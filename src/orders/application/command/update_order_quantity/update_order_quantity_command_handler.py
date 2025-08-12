from orders.application.command import UpdateOrderQuantityCommand
from orders.application.query import GetOrderByIdQuery
from orders.domain.order import Order
from orders.domain.repository.order_write_repository import OrderWriteRepository
from shared.domain.cqrs.command.icommand_handler import ICommandHandler
from shared.domain.cqrs.query.query_bus import QueryBus


class UpdateOrderQuantityCommandHandler(ICommandHandler[UpdateOrderQuantityCommand]):
    """Command handler for updating the quantity of an existing order."""

    def __init__(self, query_bus: QueryBus, repository: OrderWriteRepository):
        """
        :param repository: The order repository to use for updating orders.
        """
        self._query_bus = query_bus
        self._repository = repository

    async def handle(self, command: UpdateOrderQuantityCommand) -> None:
        """
        Handle the UpdateOrderQuantityCommand to update the quantity of an order.
        :param command: The command containing the order ID and new quantity.
        """
        order: Order = await self._query_bus.query(GetOrderByIdQuery(command.order_id))

        order.quantity = command.quantity

        await self._repository.update_order(order)
