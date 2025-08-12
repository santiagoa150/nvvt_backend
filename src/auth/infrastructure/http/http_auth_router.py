from fastapi import APIRouter, Depends, Body

from auth.application.command.create_user.create_user_command import CreateUserCommand
from auth.application.command.login_user.login_user_command import LoginUserCommand
from shared import get_command_bus
from shared.domain.cqrs.command.command_bus import CommandBus

router = APIRouter()


@router.post('/')
async def create_user(
        email: str = Body(..., description="Email of the user"),
        password: str = Body(..., description="Password of the user"),
        command_bus: CommandBus = Depends(get_command_bus)
):
    """Create a new user."""
    await command_bus.dispatch(CreateUserCommand.create(
        email=email,
        password=password,
    ))
    return {}


@router.post('/login')
async def login_user(
        email: str = Body(..., description="Email of the user"),
        password: str = Body(..., description="Password of the user"),
        command_bus: CommandBus = Depends(get_command_bus)
):
    """Login a user."""
    auth_tokens = await command_bus.dispatch(LoginUserCommand(
        email=email,
        password=password,
    ))
    return auth_tokens
