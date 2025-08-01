from campaigns.application.query.get_campaign_by_id.get_campaign_by_id_query import GetCampaignByIdQuery
from shared.infrastructure.cqrs.query.iquery_handler import IQueryHandler, Query


class GetCampaignByIdQueryHandler(IQueryHandler[GetCampaignByIdQuery]):
    """Handler for the GetCampaignByIdQuery."""

    def handle(self, query: GetCampaignByIdQuery):
        return { 'campaign_id': query.campaign_id, 'name': 'Sample Campaign' }
