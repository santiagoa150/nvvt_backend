from notifications.application.command.send_notification.send_notification_command import (
    SendNotificationCommand,
)
from notifications.domain.repository.notification_write_repository import (
    NotificationWriteRepository,
)
from notifications.infrastructure.broker.in_memory_notification_broker import (
    InMemoryNotificationBroker,
)
from shared.domain.cqrs.command.icommand_handler import ICommandHandler


class SendNotificationCommandHandler(ICommandHandler[SendNotificationCommand]):
    """Handler for the SendNotificationCommand."""

    def __init__(self, write_repository: NotificationWriteRepository, broker: InMemoryNotificationBroker):
        """
        :param write_repository: The repository used to persist the notification.
        :param broker: The broker used to publish the notification to its subscribers.
        """
        self._write_repository = write_repository
        self._broker = broker

    async def handle(self, command: SendNotificationCommand) -> None:
        """Handle the SendNotificationCommand by persisting it, then publishing it to the broker."""
        await self._write_repository.create_notification(command.notification)
        await self._broker.publish(command.notification)
