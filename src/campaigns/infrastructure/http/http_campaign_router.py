from fastapi import APIRouter, Depends

from campaigns.application.query.get_campaign_by_id.get_campaign_by_id_query import GetCampaignByIdQuery
from shared.infrastructure.cqrs.query.query_bus import QueryBus
from shared.shared_dependencies import get_query_bus

router = APIRouter()

@router.get('/{campaign_id}')
def get_campaign_by_id(campaign_id: str, query_bus: QueryBus = Depends(get_query_bus)):
    return query_bus.query(GetCampaignByIdQuery(campaign_id))
