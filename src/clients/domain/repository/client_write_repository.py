from abc import ABC, abstractmethod

from clients.domain.client import Client
from shared.domain.value_objects.id_value_object import IdValueObject


class ClientWriteRepository(ABC):
    """Abstract base class for client writing repository operations."""

    @abstractmethod
    async def create_client(self, client: Client) -> None:
        """
        Create a new client.
        :param client: The client object to create.
        """
        pass

    @abstractmethod
    async def delete_client(self, client_id: IdValueObject) -> bool:
        """
        Delete an existing client.
        :param client_id: The ID of the client to delete.
        :return: True if the client was deleted successfully, False otherwise.
        """
        pass
