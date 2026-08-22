from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCollection

from countries.application.query import GetAllCountriesQuery, GetAllCountriesQueryHandler
from countries.infrastructure.mongodb.mongodb_country_constants import (
    MongoDBCountryConstants,
)
from countries.infrastructure.mongodb.mongodb_country_read_repository import (
    MongoDBCountryReadRepository,
)
from countries.infrastructure.mongodb.mongodb_country_schema import create_country_indexes
from shared import get_mongo_client
from shared.domain.cqrs.query.query_handler import query_handler

_countries_collection: Optional[AsyncIOMotorCollection] = None
_mongo_country_read_repository: Optional[MongoDBCountryReadRepository] = None


async def get_countries_collection() -> AsyncIOMotorCollection:
    """Returns the countries collection from the MongoDB client."""

    global _countries_collection

    if _countries_collection is None:
        client = get_mongo_client()
        _countries_collection = client.db[MongoDBCountryConstants.COLLECTION_NAME.value]
        await create_country_indexes(_countries_collection)

    return _countries_collection


async def create_mongodb_country_read_repository() -> MongoDBCountryReadRepository:
    """Creates an instance of MongoDBCountryReadRepository."""

    global _mongo_country_read_repository

    if _mongo_country_read_repository is None:
        _mongo_country_read_repository = MongoDBCountryReadRepository(
            await get_countries_collection()
        )

    return _mongo_country_read_repository


@query_handler(GetAllCountriesQuery)
async def create_get_all_countries_query_handler():
    """Creates a query handler for GetAllCountriesQuery."""

    repository = await create_mongodb_country_read_repository()
    return GetAllCountriesQueryHandler(repository)
