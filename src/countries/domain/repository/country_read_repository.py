from abc import ABC, abstractmethod
from typing import List

from countries.domain.country import Country


class CountryReadRepository(ABC):
    """Abstract base class for country reading repository operations."""

    @abstractmethod
    async def get_all_countries(self) -> List[Country]:
        """
        Retrieve all countries.

        :return: A list of all countries.
        """
        pass
