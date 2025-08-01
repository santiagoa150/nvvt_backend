from typing import Type, Dict, TypeVar

from shared.infrastructure.cqrs.command.icommand import ICommand
from shared.infrastructure.cqrs.command.icommand_handler import ICommandHandler

Command = TypeVar("Command", bound=ICommand)

class CommandBus:
    """CommandBus is responsible for save and dispatching commands to their respective handlers."""

    def __init__(self):
        self._handlers: Dict[Type[ICommand], ICommandHandler] = {}

    def register_handler(self, command: Type[ICommand], handler: Type[ICommandHandler[Command]]):
        """
        Register a command handler for a specific command type.
        :param command: The command type that the handler will handle.
        :param handler: The handler class that will process the command.
        """

        if not issubclass(command, ICommand):
            raise TypeError(f"{command} must be subclass of ICommand")

        if command not in self._handlers:
            self._handlers[command] = handler()

    def dispatch(self, command: Command):
        """
        Dispatch a command to its handler and return the result.
        :param command: The command to be handled.
        """

        command_type = type(command)

        if command_type not in self._handlers:
            raise Exception(f"{command_type} not registered in CommandBus")

        handler = self._handlers[command_type]

        return handler.handle(command)