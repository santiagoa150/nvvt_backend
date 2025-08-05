import logging

from orders.application.command.delete_order.delete_order_command import DeleteOrderCommand
from orders.domain.order import Order
from orders.domain.repository.order_write_repository import OrderWriteRepository
from shared.domain.cqrs.command.icommand_handler import ICommandHandler
from shared.domain.exceptions.not_found_exception import NotFoundException


class DeleteOrderCommandHandler(ICommandHandler[DeleteOrderCommand]):
    """Command handler for deleting an order by its ID."""

    def __init__(self, repository: OrderWriteRepository):
        """
        :param repository: The order repository to use for deleting orders.
        """
        self._repository = repository
        self._logger = logging.getLogger(__name__)

    async def handle(self, command: DeleteOrderCommand) -> None:
        """
        Handle the DeleteOrderCommand to delete an order by its ID.
        :param command: The command containing the order ID.
        """
        self._logger.info(f'INIT :: Deleting order with ID: {command.order_id.str}')
        is_deleted = await self._repository.delete_order(command.order_id)
        if not is_deleted:
            raise NotFoundException.entity_not_found(Order.__name__, command.order_id.str)
