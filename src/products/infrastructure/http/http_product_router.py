from fastapi import APIRouter, BackgroundTasks, Body, Depends, Header, Request
from fastapi.security import HTTPBearer

from products.application.command import (
    CreateProductCommand,
    DeleteProductCommand,
    LoadCartCommand,
    UpdateProductQuantityCommand,
)
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


@router.patch("/{product_id}/quantity", dependencies=[Depends(bearer_scheme), Depends(jwt_guard)])
async def update_product_quantity(
    product_id: str,
    quantity: int = Body(..., embed=True, description="New quantity for the product"),
    command_bus: CommandBus = Depends(get_command_bus),
):
    """Update the quantity of a product by its ID."""
    await command_bus.dispatch(UpdateProductQuantityCommand.create(product_id, quantity))
    return {}


@router.post("/cart", dependencies=[Depends(bearer_scheme), Depends(jwt_guard)])
async def load_cart(
    request: Request,
    background_tasks: BackgroundTasks,
    x_product_provider_token: str = Header(
        ..., description="Bearer token used to authenticate against the product provider"
    ),
    cart_id: str = Body(..., description="ID of the provider's cart to load"),
    campaign_id: str = Body(..., description="ID of the campaign to load the cart into"),
    command_bus: CommandBus = Depends(get_command_bus),
):
    """
    Start loading every product from a provider's cart into a campaign in the
    background. The requesting user is notified over SSE once it finishes.
    """
    command = LoadCartCommand.create(
        campaign_id=campaign_id,
        provider_token=x_product_provider_token,
        cart_id=cart_id,
        requested_by=request.state.user["user_id"],
    )

    async def run() -> None:
        await command_bus.dispatch(command)

    background_tasks.add_task(run)
    return {}
