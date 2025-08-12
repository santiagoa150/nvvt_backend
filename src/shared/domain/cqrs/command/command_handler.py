from typing import Callable, Type

from shared.domain.cqrs.command.icommand import ICommand
from shared.domain.cqrs.command.icommand_handler import ICommandHandler

_handler_factories: dict[Type[ICommand], Callable[[], ICommandHandler[ICommand]]] = {}


def command_handler(command_type: Type[ICommand]):
    """Decorator to register a command handler factory for a specific command type."""

    def decorator(factory: Callable[[], ICommandHandler[ICommand]]):
        _handler_factories[command_type] = factory
        return factory

    return decorator


def get_registered_command_handlers():
    """Returns a dictionary of registered command handlers."""
    return _handler_factories.copy()
