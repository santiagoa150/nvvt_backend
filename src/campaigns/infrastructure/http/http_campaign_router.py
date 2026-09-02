from fastapi import APIRouter, Body, Depends, Query
from fastapi.security import HTTPBearer

from campaigns.application.command import (
    ActivateCampaignCommand,
    CreateCampaignCommand,
    DeleteCampaignCommand,
    FinishCampaignCommand,
)
from campaigns.application.query import GetCampaignSummaryQuery, GetPaginatedCampaignsQuery
from campaigns.domain.campaign import Campaign
from campaigns.domain.campaign_status import CampaignStatus
from shared import get_command_bus
from shared.domain.cqrs.command.command_bus import CommandBus
from shared.domain.cqrs.query.query_bus import QueryBus
from shared.domain.pagination_dict import PaginationDict
from shared.infrastructure.jwt.jwt_guard import jwt_guard
from shared.shared_dependencies import get_query_bus

router = APIRouter()
bearer_scheme = HTTPBearer()


@router.get("/", dependencies=[Depends(bearer_scheme), Depends(jwt_guard)])
async def get_paginated_campaigns(
    page: int = Query(1, description="Page number to retrieve"),
    limit: int = Query(20, description="Number of items per page"),
    query_bus: QueryBus = Depends(get_query_bus),
):
    """Retrieve paginated campaigns."""
    pagination: PaginationDict[Campaign] = await query_bus.query(
        GetPaginatedCampaignsQuery.create(
            page,
            limit,
        )
    )
    return PaginationDict(
        data=[campaign.to_dict() for campaign in pagination["data"]],
        metadata=pagination["metadata"],
    )


@router.post("/", dependencies=[Depends(bearer_scheme), Depends(jwt_guard)])
async def create_campaign(
    name: str = Body(..., description="Name of the campaign"),
    year: int = Body(..., description="Year of the campaign"),
    number: int = Body(..., description="Number of the campaign"),
    status: str = Body(CampaignStatus.SCHEDULED.value, description="Status of the campaign"),
    command_bus: CommandBus = Depends(get_command_bus),
):
    """Create a new campaign."""
    await command_bus.dispatch(
        CreateCampaignCommand.create(
            name=name,
            year=year,
            number=number,
            status=status,
        )
    )
    return {}


@router.get("/{campaign_id}", dependencies=[Depends(bearer_scheme), Depends(jwt_guard)])
async def get_campaign_summary(campaign_id: str, query_bus: QueryBus = Depends(get_query_bus)):
    """Retrieve a campaign's summary, including its products, by its ID."""
    return await query_bus.query(GetCampaignSummaryQuery.create(campaign_id))


@router.delete("/{campaign_id}", dependencies=[Depends(bearer_scheme), Depends(jwt_guard)])
async def delete_campaign(campaign_id: str, command_bus: CommandBus = Depends(get_command_bus)):
    """Delete a campaign by its ID."""
    await command_bus.dispatch(DeleteCampaignCommand.create(campaign_id))
    return {}


@router.patch("/{campaign_id}/activate", dependencies=[Depends(bearer_scheme), Depends(jwt_guard)])
async def activate_campaign(campaign_id: str, command_bus: CommandBus = Depends(get_command_bus)):
    """Activate a campaign by its ID."""
    await command_bus.dispatch(ActivateCampaignCommand.create(campaign_id))
    return {}


@router.patch("/{campaign_id}/finish", dependencies=[Depends(bearer_scheme), Depends(jwt_guard)])
async def finish_campaign(campaign_id: str, command_bus: CommandBus = Depends(get_command_bus)):
    """Finish a campaign by its ID. Only campaigns that are currently active can be finished."""
    await command_bus.dispatch(FinishCampaignCommand.create(campaign_id))
    return {}
