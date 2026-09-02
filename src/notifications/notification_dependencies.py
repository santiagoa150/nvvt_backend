from typing import Optional

from notifications.application.command import (
    SendNotificationCommand,
    SendNotificationCommandHandler,
)
from notifications.infrastructure.broker.in_memory_notification_broker import (
    InMemoryNotificationBroker,
)
from shared.domain.cqrs.command.command_handler import command_handler

_notification_broker: Optional[InMemoryNotificationBroker] = None


def get_notification_broker() -> InMemoryNotificationBroker:
    """Returns the singleton in-memory notification broker."""

    global _notification_broker

    if _notification_broker is None:
        _notification_broker = InMemoryNotificationBroker()

    return _notification_broker


@command_handler(SendNotificationCommand)
async def create_send_notification_command_handler() -> SendNotificationCommandHandler:
    """Creates a command handler for SendNotificationCommand."""

    broker = get_notification_broker()
    return SendNotificationCommandHandler(broker)
