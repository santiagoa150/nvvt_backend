import logging

from campaigns.application.query.get_campaign_by_id.get_campaign_by_id_query import GetCampaignByIdQuery
from campaigns.domain.campaign import Campaign
from campaigns.domain.repository.campaign_read_repository import CampaignReadRepository
from shared.domain.cqrs.query.iquery_handler import IQueryHandler
from shared.domain.exceptions.not_found_exception import NotFoundException


class GetCampaignByIdQueryHandler(IQueryHandler[GetCampaignByIdQuery]):
    """Handler for the GetCampaignByIdQuery."""

    def __init__(self, repository: CampaignReadRepository):
        """
        :param repository: The campaign repository to use for fetching campaigns.
        """
        self._repository = repository
        self._logger = logging.getLogger(__name__)

    async def handle(self, query: GetCampaignByIdQuery) -> Campaign:
        """
        Handle the GetCampaignByIdQuery to retrieve a campaign by its ID.
        :param query: The query containing the campaign ID.
        :return: The campaign associated with the provided ID.
        :raises NotFoundException: If no campaign is found with the provided ID.
        """
        self._logger.info(f'INIT :: CampaignID: {query.campaign_id.str}')
        campaign = await self._repository.get_campaign_by_id(query.campaign_id)

        if not campaign:
            raise NotFoundException.entity_not_found(Campaign.__name__, query.campaign_id.str)

        return campaign
