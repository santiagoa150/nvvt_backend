import logging

from orders.application.query import GetOrderByIdQuery
from orders.domain.order import Order
from orders.domain.repository.order_read_repository import OrderReadRepository
from shared.domain.cqrs.query.iquery_handler import IQueryHandler
from shared.domain.exceptions.not_found_exception import NotFoundException


class GetOrderByIdQueryHandler(IQueryHandler[GetOrderByIdQuery]):
    """Handler for the GetOrderByIdQuery."""

    def __init__(self, repository: OrderReadRepository):
        """
        :param repository: The order repository to use for fetching orders.
        """
        self._repository = repository
        self._logger = logging.getLogger(__name__)

    async def handle(self, query: GetOrderByIdQuery):
        """
        Handle the GetOrderByIdQuery to retrieve an order by its ID.

        :param query: The query containing the order ID.
        :return: The order associated with the provided ID.
        """
        self._logger.info(f"INIT :: OrderID: {query.order_id.str}")
        order = await self._repository.get_order_by_id(query.order_id)

        if not order:
            raise NotFoundException.entity_not_found(Order.__name__, query.order_id.str)

        return order
