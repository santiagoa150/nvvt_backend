from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from shared.infrastructure.cqrs.command.icommand import ICommand

Command = TypeVar('Command', bound=ICommand)

class ICommandHandler(ABC, Generic[Command]):
    """Interface for a command handler in the CQRS pattern."""

    @abstractmethod
    def handle(self, command: Command):
        """Handle the given command and return the result."""
        pass