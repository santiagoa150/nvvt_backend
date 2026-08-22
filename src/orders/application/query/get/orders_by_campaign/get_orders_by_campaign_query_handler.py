import logging

from orders.application.query import GetOrdersByCampaignQuery
from orders.domain.order import Order
from orders.domain.repository.order_read_repository import OrderReadRepository
from products.application.query import GetProductsByCampaignQuery
from shared.domain.cqrs.query.iquery_handler import IQueryHandler
from shared.domain.cqrs.query.query_bus import QueryBus


class GetOrdersByCampaignQueryHandler(IQueryHandler[GetOrdersByCampaignQuery]):
    """Handler for the GetOrdersByCampaignQuery."""

    def __init__(self, query_bus: QueryBus, repository: OrderReadRepository):
        """
        :param query_bus: The query bus to use for resolving the campaign's products.
        :param repository: The order repository to use for fetching orders.
        """
        self._query_bus = query_bus
        self._repository = repository
        self._logger = logging.getLogger(__name__)

    async def handle(self, query: GetOrdersByCampaignQuery) -> dict[str, list[Order]]:
        """
        Handle the GetOrdersByCampaignQuery to retrieve orders by campaign ID.

        :param query: The query containing the campaign ID.
        :return: A dictionary grouping orders by their status.
        """
        self._logger.info(
            f"INIT :: Getting All Orders by "
            f"CampaignID: {query.campaign_id.str} "
            f"and ClientID: {query.client_id.str if query.client_id else None}"
        )

        products = await self._query_bus.query(GetProductsByCampaignQuery(query.campaign_id))
        product_ids = [product.product_id for product in products]

        return await self._repository.get_orders_by_product_ids(product_ids, query.client_id)
