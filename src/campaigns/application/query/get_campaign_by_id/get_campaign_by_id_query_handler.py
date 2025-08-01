from campaigns.application.query.get_campaign_by_id.get_campaign_by_id_query import GetCampaignByIdQuery
from shared.domain.cqrs.query.iquery_handler import IQueryHandler


class GetCampaignByIdQueryHandler(IQueryHandler[GetCampaignByIdQuery]):
    """Handler for the GetCampaignByIdQuery."""

    def handle(self, query: GetCampaignByIdQuery):
        return { 'campaign_id': query.campaign_id, 'name': 'Sample Campaign' }
