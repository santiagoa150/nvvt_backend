import logging
from typing import List

from campaigns.application.query.get.campaign_summary.campaign_with_products_dict import (
    CampaignWithProductsDict,
)
from campaigns.application.query.get.campaign_summary.get_campaign_summary_query import (
    GetCampaignSummaryQuery,
)
from campaigns.domain.campaign import Campaign
from campaigns.domain.campaign_summary import CampaignSummary
from campaigns.domain.repository.campaign_read_repository import CampaignReadRepository
from products.application.query.get.products_by_campaign.get_products_by_campaign_query import (
    GetProductsByCampaignQuery,
)
from products.domain.product import Product
from shared.domain.cqrs.query.iquery_handler import IQueryHandler
from shared.domain.cqrs.query.query_bus import QueryBus
from shared.domain.exceptions.not_found_exception import NotFoundException


class GetCampaignSummaryQueryHandler(IQueryHandler[GetCampaignSummaryQuery]):
    """Handler for the GetCampaignSummaryQuery."""

    def __init__(self, repository: CampaignReadRepository, query_bus: QueryBus):
        """
        :param repository: The campaign repository to use for fetching the campaign.
        :param query_bus: The query bus used to fetch the campaign's products.
        """
        self._repository = repository
        self._query_bus = query_bus
        self._logger = logging.getLogger(__name__)

    async def handle(self, query: GetCampaignSummaryQuery) -> CampaignWithProductsDict:
        """
        Handle the GetCampaignSummaryQuery to retrieve a campaign, along with its
        products and their pricing summary, by its ID.

        :param query: The query containing the campaign ID.
        :return: The campaign, its products, and their calculated pricing summary.
        :raises NotFoundException: If no campaign is found with the provided ID.
        """
        self._logger.info(f"INIT :: CampaignID: {query.campaign_id.str}")
        campaign = await self._repository.get_campaign_by_id(query.campaign_id)

        if not campaign:
            raise NotFoundException.entity_not_found(Campaign.__name__, query.campaign_id.str)

        products: List[Product] = await self._query_bus.query(
            GetProductsByCampaignQuery(query.campaign_id)
        )
        summary = CampaignSummary.calculate(products)

        return CampaignWithProductsDict(
            **campaign.to_dict(),
            products=[product.to_dict() for product in products],
            summary=summary.to_dict(),
        )
