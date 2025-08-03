from campaigns.application.query.get_campaign_by_id.get_campaign_by_id_query import GetCampaignByIdQuery
from campaigns.application.query.get_campaign_by_id.get_campaign_by_id_query_handler import GetCampaignByIdQueryHandler
from campaigns.application.query.get_paginated_campaigns.get_paginated_campaigns_query import GetPaginatedCampaignsQuery
from campaigns.application.query.get_paginated_campaigns.get_paginated_campaigns_query_handler import \
    GetPaginatedCampaignsQueryHandler
from campaigns.domain.repository.campaign_repository import CampaignRepository
from campaigns.infrastructure.mongodb.mongodb_campaign_constants import MongoDBCampaignConstants
from campaigns.infrastructure.mongodb.mongodb_campaign_repository import MongoDBCampaignRepository
from shared import get_mongo_client
from shared.domain.cqrs.query.query_handler import query_handler

_mongo_campaign_repository: MongoDBCampaignRepository | None = None


def create_mongodb_campaign_repository() -> MongoDBCampaignRepository:
    """Creates an instance of MongoDBCampaignRepository."""

    client = get_mongo_client()

    global _mongo_campaign_repository

    if _mongo_campaign_repository is None:
        _mongo_campaign_repository = MongoDBCampaignRepository(
            client.db[MongoDBCampaignConstants.COLLECTION_NAME.value]
        )

    return _mongo_campaign_repository


@query_handler(GetCampaignByIdQuery)
def create_get_campaign_by_id_query_handler() -> GetCampaignByIdQueryHandler:
    """
    Creates a query handler for GetCampaignByIdQuery.
    This function is decorated with `@query_handler` to register the handler with the query bus automatically.
    """
    repository: CampaignRepository = create_mongodb_campaign_repository()
    return GetCampaignByIdQueryHandler(repository)


@query_handler(GetPaginatedCampaignsQuery)
def create_get_paginated_campaigns_query_handler() -> GetPaginatedCampaignsQueryHandler:
    """
    Creates a query handler for GetPaginatedCampaignsQuery.
    This function is decorated with `@query_handler` to register the handler with the query bus automatically.
    """
    repository: CampaignRepository = create_mongodb_campaign_repository()
    return GetPaginatedCampaignsQueryHandler(repository)
