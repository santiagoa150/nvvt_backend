from fastapi import APIRouter, Depends

from campaigns.application.query.get_campaign_by_id.get_campaign_by_id_query import GetCampaignByIdQuery
from campaigns.domain.campaign import Campaign
from shared.domain.cqrs.query.query_bus import QueryBus
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.shared_dependencies import get_query_bus

router = APIRouter()


@router.get('/{campaign_id}')
def get_campaign_by_id(campaign_id: str, query_bus: QueryBus = Depends(get_query_bus)):
    print("Hola")
    campaign: Campaign = query_bus.query(GetCampaignByIdQuery(
        IdValueObject(campaign_id),
    ))
    return campaign.to_dict()
