from fastapi import APIRouter, Depends, Query, Body, Header
from fastapi.security import HTTPBearer

from orders.application.command import CreateOrderCommand, DeleteOrderCommand, UpdateOrderQuantityCommand
from orders.application.query import GetOrderByIdQuery, GetOrdersByCampaignQuery
from orders.domain.order import Order
from shared import get_query_bus, get_command_bus
from shared.domain.cqrs.command.command_bus import CommandBus
from shared.domain.cqrs.query.query_bus import QueryBus
from shared.infrastructure.jwt.jwt_guard import jwt_guard

router = APIRouter()
bearer_scheme = HTTPBearer()


@router.post('/', dependencies=[Depends(bearer_scheme), Depends(jwt_guard)])
async def create_order(
        x_session_id: str = Header(..., description="Provided session ID for the request"),
        x_route: str = Header(..., description="Provider route for the request"),
        x_accelerator_secure_guid: str = Header(..., description="Provider accelerator secure GUID"),
        x_cebs_p: str = Header(..., description="Provider cebs p"),
        x_cebs: str = Header(..., description="Provider cebs"),
        product_url: str = Body(..., description='URL of the product to order'),
        campaign_id: str = Body(..., description='Campaign ID for the order'),
        client_id: str = Body(..., description='Client ID placing the order'),
        quantity: int = Body(..., description='Quantity of the product to order'),
        status: str = Body(..., description='Optional status for the order'),
        command_bus: CommandBus = Depends(get_command_bus)
):
    """Endpoint to create a new order."""
    await command_bus.dispatch(CreateOrderCommand.create(
        session_id=x_session_id,
        route=x_route,
        accelerator_secure_guid=x_accelerator_secure_guid,
        cebs_p=x_cebs_p,
        cebs=x_cebs,
        product_url=product_url,
        campaign_id=campaign_id,
        client_id=client_id,
        quantity=quantity,
        status=status
    ))
    return {}


@router.get('/{order_id}', dependencies=[Depends(bearer_scheme), Depends(jwt_guard)])
async def get_order_by_id(order_id: str, query_bus: QueryBus = Depends(get_query_bus)):
    """Retrieve an order by its ID."""
    order: Order = await query_bus.query(GetOrderByIdQuery.create(order_id))
    return order.to_dict()


@router.delete('/{order_id}', dependencies=[Depends(bearer_scheme), Depends(jwt_guard)])
async def delete_order_by_id(order_id: str, command_bus: CommandBus = Depends(get_command_bus)):
    """Delete an order by its ID."""
    await command_bus.dispatch(DeleteOrderCommand.create(order_id))
    return {}


@router.patch('/{order_id}/quantity', dependencies=[Depends(bearer_scheme), Depends(jwt_guard)])
async def update_order_quantity(
        order_id: str,
        quantity: int = Body(..., description='New quantity for the order'),
        command_bus: CommandBus = Depends(get_command_bus)
):
    """Update the quantity of an existing order."""
    await command_bus.dispatch(UpdateOrderQuantityCommand.create(order_id, quantity))
    return {}


@router.get('/by-campaign/{campaign_id}', dependencies=[Depends(bearer_scheme), Depends(jwt_guard)])
async def get_orders_by_campaign(
        campaign_id: str,
        client_id: str = Query(None, description='Optional client ID to filter orders'),
        query_bus: QueryBus = Depends(get_query_bus)
):
    """Retrieve orders by campaign ID."""
    orders: dict[str, list[Order]] = await query_bus.query(GetOrdersByCampaignQuery.create(campaign_id, client_id))
    return {k: [order.to_dict() for order in v] for k, v in orders.items()}
