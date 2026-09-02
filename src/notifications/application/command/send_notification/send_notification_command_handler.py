from notifications.application.command.send_notification.send_notification_command import (
    SendNotificationCommand,
)
from notifications.infrastructure.broker.in_memory_notification_broker import (
    InMemoryNotificationBroker,
)
from shared.domain.cqrs.command.icommand_handler import ICommandHandler


class SendNotificationCommandHandler(ICommandHandler[SendNotificationCommand]):
    """Handler for the SendNotificationCommand."""

    def __init__(self, broker: InMemoryNotificationBroker):
        """
        :param broker: The broker used to publish the notification to its subscribers.
        """
        self._broker = broker

    async def handle(self, command: SendNotificationCommand) -> None:
        """Handle the SendNotificationCommand by publishing it to the broker."""
        await self._broker.publish(command.notification)
