from fastapi import APIRouter, Body, Depends, Header
from fastapi.security import HTTPBearer

from products.application.command import CreateProductCommand, DeleteProductCommand
from shared import get_command_bus
from shared.domain.cqrs.command.command_bus import CommandBus
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


@router.delete("/{product_id}", dependencies=[Depends(bearer_scheme), Depends(jwt_guard)])
async def delete_product(product_id: str, command_bus: CommandBus = Depends(get_command_bus)):
    """Delete a product by its ID."""
    await command_bus.dispatch(DeleteProductCommand.create(product_id))
    return {}
