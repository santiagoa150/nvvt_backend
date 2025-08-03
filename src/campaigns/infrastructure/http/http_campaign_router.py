from fastapi import APIRouter, Depends, Query

from campaigns.application.query.get_campaign_by_id.get_campaign_by_id_query import GetCampaignByIdQuery
from campaigns.application.query.get_paginated_campaigns.get_paginated_campaigns_query import GetPaginatedCampaignsQuery
from campaigns.domain.campaign import Campaign
from shared.domain.cqrs.query.query_bus import QueryBus
from shared.domain.pagination_dict import PaginationDict
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.pagination.limit_param import LimitParam
from shared.domain.value_objects.pagination.page_param import PageParam
from shared.shared_dependencies import get_query_bus

router = APIRouter()


@router.get('/')
async def get_paginated_campaigns(
        page: int = Query(1, description="Page number to retrieve"),
        limit: int = Query(20, description="Number of items per page"),
        query_bus: QueryBus = Depends(get_query_bus)
):
    """Retrieve paginated campaigns."""
    pagination: PaginationDict[Campaign] = await query_bus.query(GetPaginatedCampaignsQuery(
        PageParam(page),
        LimitParam(float(limit)),
    ))
    return PaginationDict(data=[campaign.to_dict() for campaign in pagination['data']], metadata=pagination['metadata'])


@router.get('/{campaign_id}')
async def get_campaign_by_id(campaign_id: str, query_bus: QueryBus = Depends(get_query_bus)):
    """Retrieve a campaign by its ID."""
    campaign: Campaign = await query_bus.query(GetCampaignByIdQuery(
        IdValueObject(campaign_id),
    ))
    return campaign.to_dict()
