import asyncio
from collections import defaultdict
from typing import Dict, List

from notifications.domain.notification import Notification


class InMemoryNotificationBroker:
    """
    In-memory publish/subscribe broker that fans out notifications to every
    active subscriber of their recipient. Subscribers are per-process, in
    memory, and not persisted: a notification published while a recipient has
    no active subscriber is simply dropped.
    """

    def __init__(self):
        self._subscribers: Dict[str, List["asyncio.Queue[Notification]"]] = defaultdict(list)

    def subscribe(self, recipient: str) -> "asyncio.Queue[Notification]":
        """Registers and returns a new subscriber queue for the given recipient."""
        queue: "asyncio.Queue[Notification]" = asyncio.Queue()
        self._subscribers[recipient].append(queue)
        return queue

    def unsubscribe(self, recipient: str, queue: "asyncio.Queue[Notification]") -> None:
        """Removes a previously registered subscriber queue for the given recipient."""
        subscribers = self._subscribers.get(recipient)
        if not subscribers or queue not in subscribers:
            return

        subscribers.remove(queue)
        if not subscribers:
            del self._subscribers[recipient]

    async def publish(self, notification: Notification) -> None:
        """Delivers a notification to every active subscriber of its recipient."""
        for queue in self._subscribers.get(notification.recipient.str, []):
            await queue.put(notification)
