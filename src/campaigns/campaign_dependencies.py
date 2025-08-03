from campaigns.application.query.get_campaign_by_id.get_campaign_by_id_query import GetCampaignByIdQuery
from campaigns.application.query.get_campaign_by_id.get_campaign_by_id_query_handler import GetCampaignByIdQueryHandler
from campaigns.domain.repository.campaign_repository import CampaignRepository
from campaigns.infrastructure.mongodb.mongodb_campaign_repository import MongoDBCampaignRepository
from shared.domain.cqrs.query.query_handler import query_handler

_mongo_campaign_repository: MongoDBCampaignRepository | None = None


def create_mongodb_campaign_repository() -> MongoDBCampaignRepository:
    """Creates an instance of MongoDBCampaignRepository."""

    global _mongo_campaign_repository

    if _mongo_campaign_repository is None:
        _mongo_campaign_repository = MongoDBCampaignRepository()

    return _mongo_campaign_repository


@query_handler(GetCampaignByIdQuery)
def create_get_campaign_by_id_query_handler() -> GetCampaignByIdQueryHandler:
    """
    Creates a query handler for GetCampaignByIdQuery.
    This function is decorated with `@query_handler` to register the handler with the query bus automatically.
    """
    repository: CampaignRepository = create_mongodb_campaign_repository()
    return GetCampaignByIdQueryHandler(repository)
