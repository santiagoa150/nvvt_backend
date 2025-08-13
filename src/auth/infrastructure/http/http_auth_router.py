from fastapi import APIRouter, Body, Depends
from fastapi.params import Header

from auth.application.command import (
    CreateUserCommand,
    LoginUserCommand,
    RefreshUserAuthTokensCommand,
)
from shared import get_command_bus
from shared.domain.cqrs.command.command_bus import CommandBus

router = APIRouter()


@router.post("/")
async def create_user(
    email: str = Body(..., description="Email of the user"),
    password: str = Body(..., description="Password of the user"),
    command_bus: CommandBus = Depends(get_command_bus),
):
    """Create a new user."""
    await command_bus.dispatch(
        CreateUserCommand.create(
            email=email,
            password=password,
        )
    )
    return {}


@router.post("/login")
async def login_user(
    email: str = Body(..., description="Email of the user"),
    password: str = Body(..., description="Password of the user"),
    command_bus: CommandBus = Depends(get_command_bus),
):
    """Login a user."""
    auth_tokens = await command_bus.dispatch(
        LoginUserCommand(
            email=email,
            password=password,
        )
    )
    return auth_tokens


@router.post("/refresh")
async def refresh_user_auth_tokens(
    refresh_token: str = Header(..., description="Refresh token of the user"),
    command_bus: CommandBus = Depends(get_command_bus),
):
    """Refresh user authentication tokens."""
    auth_tokens = await command_bus.dispatch(RefreshUserAuthTokensCommand(refresh_token))
    return auth_tokens
