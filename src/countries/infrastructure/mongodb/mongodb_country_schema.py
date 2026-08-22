from motor.motor_asyncio import AsyncIOMotorCollection


async def create_country_indexes(collection: AsyncIOMotorCollection) -> None:
    """Creates indexes for the countries collection."""
    await collection.create_index("country_code", unique=True)
