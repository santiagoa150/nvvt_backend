from abc import ABC, abstractmethod
from typing import Optional

from clients.domain.client import Client
from shared.domain.value_objects.id_value_object import IdValueObject


class ClientReadRepository(ABC):
    """Abstract base class for client reading repository operations."""

    @abstractmethod
    async def get_client_by_id(self, client_id: IdValueObject) -> Optional[Client]:
        """
        Retrieve a client by its ID.

        :param client_id: The ID of the client to retrieve.
        :return: A dictionary representation of the client.
        """
        pass
