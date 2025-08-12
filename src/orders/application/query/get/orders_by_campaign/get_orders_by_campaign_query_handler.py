import logging
from collections.abc import Awaitable

from orders.application.query.get.orders_by_campaign.get_orders_by_campaign_query import GetOrdersByCampaignQuery
from orders.domain.order import Order
from orders.domain.repository.order_read_repository import OrderReadRepository
from shared.domain.cqrs.query.iquery_handler import IQueryHandler


class GetOrdersByCampaignQueryHandler(IQueryHandler[GetOrdersByCampaignQuery]):
    """Handler for the GetOrdersByCampaignQuery."""

    def __init__(self, repository: OrderReadRepository):
        """
        :param repository: The order repository to use for fetching orders.
        """
        self._repository = repository
        self._logger = logging.getLogger(__name__)

    def handle(self, query: GetOrdersByCampaignQuery) -> Awaitable[dict[str, list[Order]]]:
        """
        Handle the GetOrdersByCampaignQuery to retrieve orders by campaign ID.

        :param query: The query containing the campaign ID.
        :return: A list of orders associated with the provided campaign ID.
        """
        self._logger.info(f'INIT :: Getting All Orders by '
                          f'CampaignID: {query.campaign_id.str} '
                          f'and ClientID: {query.client_id.str if query.client_id else None}')
        return self._repository.get_orders_by_campaign(query.campaign_id, query.client_id)
