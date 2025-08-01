from typing import Type, Dict, TypeVar

from shared.domain.cqrs.command.icommand import ICommand
from shared.domain.cqrs.command.icommand_handler import ICommandHandler
from shared.domain.exceptions.common_exception_messages import CommonExceptionMessages
from shared.domain.exceptions.cqrs_exception import CqrsException

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
            raise CqrsException(CommonExceptionMessages.INVALID_COMMAND_SUB_CLASS.format(command=command))

        if command not in self._handlers:
            self._handlers[command] = handler()

    def dispatch(self, command: Command):
        """
        Dispatch a command to its handler and return the result.
        :param command: The command to be handled.
        """

        command_type = type(command)

        if command_type not in self._handlers:
            raise CqrsException(CommonExceptionMessages.COMMAND_NOT_REGISTERED.format(command_type=command_type))

        handler = self._handlers[command_type]

        return handler.handle(command)
