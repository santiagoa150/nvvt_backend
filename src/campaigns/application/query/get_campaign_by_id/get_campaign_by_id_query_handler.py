from campaigns.application.query.get_campaign_by_id.get_campaign_by_id_query import GetCampaignByIdQuery
from campaigns.domain.campaign import Campaign
from campaigns.domain.repository.campaign_repository import CampaignRepository
from shared.domain.cqrs.query.iquery_handler import IQueryHandler
from shared.domain.exceptions.common_exception_messages import CommonExceptionMessages
from shared.domain.exceptions.not_found_exception import NotFoundException


class GetCampaignByIdQueryHandler(IQueryHandler[GetCampaignByIdQuery]):
    """Handler for the GetCampaignByIdQuery."""

    def __init__(self, repository: CampaignRepository):
        """
        :param repository: The campaign repository to use for fetching campaigns.
        """
        self._repository = repository

    def handle(self, query: GetCampaignByIdQuery) -> Campaign:
        """
        Handle the GetCampaignByIdQuery to retrieve a campaign by its ID.
        :param query: The query containing the campaign ID.
        :return: The campaign associated with the provided ID.
        :raises NotFoundException: If no campaign is found with the provided ID.
        """
        campaign = self._repository.get_campaign_by_id(query.campaign_id)

        if not campaign:
            raise NotFoundException(
                CommonExceptionMessages.ENTITY_NOT_FOUND.format(entity=Campaign.__name__, id=query.campaign_id.str)
            )

        return campaign
