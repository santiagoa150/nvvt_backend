from abc import ABC, abstractmethod

from clients.domain.client import Client


class ClientWriteRepository(ABC):
    """Abstract base class for client writing repository operations."""

    @abstractmethod
    async def create_client(self, client: Client) -> None:
        """Create a new client."""
        pass
