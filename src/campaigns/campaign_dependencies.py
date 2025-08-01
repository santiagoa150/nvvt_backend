from campaigns.application.query.get_campaign_by_id.get_campaign_by_id_query import GetCampaignByIdQuery
from campaigns.application.query.get_campaign_by_id.get_campaign_by_id_query_handler import GetCampaignByIdQueryHandler
from shared.infrastructure.cqrs.query.query_handler import query_handler


@query_handler(GetCampaignByIdQuery)
def create_get_campaign_by_id_query_handler() -> GetCampaignByIdQueryHandler:
    """
    Creates a query handler for GetCampaignByIdQuery.
    This function is decorated with `@query_handler` to register the handler with the query bus automatically.
    """
    return GetCampaignByIdQueryHandler()
