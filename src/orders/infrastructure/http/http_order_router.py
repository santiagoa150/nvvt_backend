from fastapi import APIRouter, Depends

from orders.application.query.get_order_by_id.get_order_by_id_query import GetOrderByIdQuery
from orders.domain.order import Order
from shared import get_query_bus

router = APIRouter()


@router.get('/{order_id}')
async def get_order_by_id(order_id: str, query_bus=Depends(get_query_bus)):
    """Retrieve an order by its ID."""
    order: Order = await query_bus.query(GetOrderByIdQuery.create(order_id))
    return order.to_dict()
