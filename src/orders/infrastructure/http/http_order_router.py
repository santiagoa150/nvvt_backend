from fastapi import APIRouter, Depends

from orders.application.query.get_order_by_id.get_order_by_id_query import GetOrderByIdQuery
from orders.application.query.get_orders_by_campaign.get_orders_by_campaign_query import GetOrdersByCampaignQuery
from orders.domain.order import Order
from shared import get_query_bus

router = APIRouter()


@router.get('/{order_id}')
async def get_order_by_id(order_id: str, query_bus=Depends(get_query_bus)):
    """Retrieve an order by its ID."""
    order: Order = await query_bus.query(GetOrderByIdQuery.create(order_id))
    return order.to_dict()


@router.get('/by-campaign/{campaign_id}')
async def get_orders_by_campaign(campaign_id: str, query_bus=Depends(get_query_bus)):
    """Retrieve orders by campaign ID."""
    orders: list[Order] = await query_bus.query(GetOrdersByCampaignQuery.create(campaign_id))
    return [order.to_dict() for order in orders]
