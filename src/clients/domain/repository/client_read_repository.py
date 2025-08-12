from abc import ABC, abstractmethod
from typing import Optional

from clients.domain.client import Client
from shared.domain.pagination_dict import PaginationDict
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.pagination.limit_param import LimitParam
from shared.domain.value_objects.pagination.page_param import PageParam


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

    @abstractmethod
    async def get_paginated_clients(
        self, page: PageParam, limit: LimitParam
    ) -> PaginationDict[Client]:
        """
        Retrieve paginated clients.

        :param page: The page number to retrieve.
        :param limit: The number of items per page.
        :return: A PaginationDict containing the paginated clients.
        """
        pass
