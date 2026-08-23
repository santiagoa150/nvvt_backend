from typing import List

from fastapi import APIRouter, Body, Depends, Header
from fastapi.security import HTTPBearer

from products.application.command import CreateProductCommand
from products.application.query import GetProductsByCampaignQuery
from products.domain.product import Product
from shared import get_command_bus, get_query_bus
from shared.domain.cqrs.command.command_bus import CommandBus
from shared.domain.cqrs.query.query_bus import QueryBus
from shared.infrastructure.jwt.jwt_guard import jwt_guard

router = APIRouter()
bearer_scheme = HTTPBearer()


@router.post("/", dependencies=[Depends(bearer_scheme), Depends(jwt_guard)])
async def create_product(
    x_product_provider_token: str = Header(
        ..., description="Bearer token used to authenticate against the product provider"
    ),
    code: str = Body(..., description="Code of the product to create"),
    quantity: int = Body(..., description="Quantity of the product"),
    campaign_id: str = Body(..., description="ID of the campaign the product belongs to"),
    command_bus: CommandBus = Depends(get_command_bus),
):
    """Create a new product for a campaign."""
    await command_bus.dispatch(
        CreateProductCommand.create(
            provider_token=x_product_provider_token,
            code=code,
            quantity=quantity,
            campaign_id=campaign_id,
        )
    )
    return {}


@router.get("/campaign/{campaign_id}", dependencies=[Depends(bearer_scheme), Depends(jwt_guard)])
async def get_products_by_campaign(campaign_id: str, query_bus: QueryBus = Depends(get_query_bus)):
    """Retrieve all products belonging to a campaign."""
    products: List[Product] = await query_bus.query(GetProductsByCampaignQuery.create(campaign_id))
    return [product.to_dict() for product in products]
