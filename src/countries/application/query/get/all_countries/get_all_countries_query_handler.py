import logging
from typing import List

from countries.application.query.get.all_countries.get_all_countries_query import (
    GetAllCountriesQuery,
)
from countries.domain.country import Country
from countries.domain.repository.country_read_repository import CountryReadRepository
from shared.domain.cqrs.query.iquery_handler import IQueryHandler


class GetAllCountriesQueryHandler(IQueryHandler[GetAllCountriesQuery]):
    """Handler for the GetAllCountriesQuery."""

    def __init__(self, repository: CountryReadRepository):
        """
        :param repository: The country repository to use for fetching countries.
        """
        self._repository = repository
        self._logger = logging.getLogger(__name__)

    async def handle(self, query: GetAllCountriesQuery) -> List[Country]:
        """
        Handle the GetAllCountriesQuery to retrieve all countries.

        :param query: The query requesting all countries.
        :return: The list of all countries.
        """
        self._logger.info("INIT :: Retrieving all countries")
        return await self._repository.get_all_countries()
