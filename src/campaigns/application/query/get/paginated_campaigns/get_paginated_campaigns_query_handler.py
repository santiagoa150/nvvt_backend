import logging
from typing import Awaitable

from campaigns.application.query.get.paginated_campaigns.get_paginated_campaigns_query import GetPaginatedCampaignsQuery
from campaigns.domain.campaign import Campaign
from campaigns.domain.repository.campaign_read_repository import CampaignReadRepository
from shared.domain.cqrs.query.iquery_handler import IQueryHandler
from shared.domain.pagination_dict import PaginationDict


class GetPaginatedCampaignsQueryHandler(IQueryHandler[GetPaginatedCampaignsQuery]):
    """Handler for the GetPaginatedCampaignsQuery."""

    def __init__(self, repository: CampaignReadRepository):
        """
        :param repository: The campaign repository to use for fetching campaigns.
        """
        self._repository = repository
        self._logger = logging.getLogger(__name__)

    def handle(self, query: GetPaginatedCampaignsQuery) -> Awaitable[PaginationDict[Campaign]]:
        """
        Handle the GetPaginatedCampaignsQuery to retrieve paginated campaigns.
        :param query: The query containing pagination parameters.
        :return: A list of campaigns for the requested page.
        """
        self._logger.info(f'INIT :: Getting All Campaigns with Page: {query.page}, Limit: {query.limit}')
        return self._repository.get_paginated_campaigns(query.page, query.limit)
