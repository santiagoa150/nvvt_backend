from typing import List, cast

from motor.motor_asyncio import AsyncIOMotorCollection

from countries.domain.country import Country
from countries.domain.country_dict import CountryDict
from countries.domain.repository.country_read_repository import CountryReadRepository


class MongoDBCountryReadRepository(CountryReadRepository):
    """MongoDB implementation of the CountryReadRepository interface for reading country data."""

    def __init__(self, collection: AsyncIOMotorCollection):
        """Initializes the MongoDBCountryReadRepository with a MongoDB collection."""
        self._collection = collection

    async def get_all_countries(self) -> List[Country]:
        """Retrieves all countries from the MongoDB countries collection, sorted by name."""
        cursor = self._collection.find({}).sort("country_name", 1)
        documents = await cursor.to_list(length=None)
        return [Country.from_dict(cast(CountryDict, document)) for document in documents]
