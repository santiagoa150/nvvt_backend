import logging
from typing import List

from products.application.query.get.products_by_campaign.get_products_by_campaign_query import (
    GetProductsByCampaignQuery,
)
from products.domain.product import Product
from products.domain.repository.product_read_repository import ProductReadRepository
from shared.domain.cqrs.query.iquery_handler import IQueryHandler


class GetProductsByCampaignQueryHandler(IQueryHandler[GetProductsByCampaignQuery]):
    """Handler for the GetProductsByCampaignQuery."""

    def __init__(self, repository: ProductReadRepository):
        """
        :param repository: The product repository to use for fetching products.
        """
        self._repository = repository
        self._logger = logging.getLogger(__name__)

    async def handle(self, query: GetProductsByCampaignQuery) -> List[Product]:
        """
        Handle the GetProductsByCampaignQuery to retrieve all products for a campaign.

        :param query: The query containing the campaign ID.
        :return: The list of products belonging to the campaign.
        """
        self._logger.info(f"INIT :: CampaignID: {query.campaign_id.str}")
        return await self._repository.get_products_by_campaign_id(query.campaign_id)
