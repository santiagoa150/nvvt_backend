from fastapi import APIRouter, Depends, Query, Body

from campaigns.application.command.create_campaign.create_campaign_command import CreateCampaignCommand
from campaigns.application.query.get_campaign_by_id.get_campaign_by_id_query import GetCampaignByIdQuery
from campaigns.application.query.get_paginated_campaigns.get_paginated_campaigns_query import GetPaginatedCampaignsQuery
from campaigns.domain.campaign import Campaign
from campaigns.domain.campaign_dict import CampaignDict
from campaigns.domain.value_objects.campaign_number import CampaignNumber
from shared import get_command_bus
from shared.domain.cqrs.command.command_bus import CommandBus
from shared.domain.cqrs.query.query_bus import QueryBus
from shared.domain.pagination_dict import PaginationDict
from shared.domain.value_objects.common.year import Year
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.pagination.limit_param import LimitParam
from shared.domain.value_objects.pagination.page_param import PageParam
from shared.domain.value_objects.string_value_object import StringValueObject
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
    return PaginationDict(
        data=[campaign.to_dict() for campaign in pagination['data']],
        metadata=pagination['metadata'],
    )


@router.post('/')
async def create_campaign(
        name: str = Body(..., description="Name of the campaign"),
        year: int = Body(..., description="Year of the campaign"),
        number: int = Body(..., description="Number of the campaign"),
        command_bus: CommandBus = Depends(get_command_bus)
):
    """Create a new campaign."""
    await command_bus.dispatch(CreateCampaignCommand(
        StringValueObject(name),
        Year(year),
        CampaignNumber(number),
    ))
    return {}


@router.get('/{campaign_id}')
async def get_campaign_by_id(campaign_id: str, query_bus: QueryBus = Depends(get_query_bus)):
    """Retrieve a campaign by its ID."""
    campaign: Campaign = await query_bus.query(GetCampaignByIdQuery(
        IdValueObject(campaign_id),
    ))
    return campaign.to_dict()
