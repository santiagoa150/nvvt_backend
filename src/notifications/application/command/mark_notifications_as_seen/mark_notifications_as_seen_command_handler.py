from notifications.application.command.mark_notifications_as_seen.mark_notifications_as_seen_command import (
    MarkNotificationsAsSeenCommand,
)
from notifications.domain.repository.notification_write_repository import (
    NotificationWriteRepository,
)
from shared.domain.cqrs.command.icommand_handler import ICommandHandler


class MarkNotificationsAsSeenCommandHandler(ICommandHandler[MarkNotificationsAsSeenCommand]):
    """Handler for the MarkNotificationsAsSeenCommand."""

    def __init__(self, write_repository: NotificationWriteRepository):
        """
        :param write_repository: The repository used to mark the notifications as seen.
        """
        self._write_repository = write_repository

    async def handle(self, command: MarkNotificationsAsSeenCommand) -> None:
        """Handle the MarkNotificationsAsSeenCommand by marking the notifications as seen."""
        await self._write_repository.mark_as_seen(command.notification_ids)
