from motor.motor_asyncio import AsyncIOMotorCollection


async def create_product_indexes(collection: AsyncIOMotorCollection) -> None:
    """Creates indexes for the products collection."""
    await collection.create_index("product_id", unique=True)
    # A product's code is only unique within its own campaign.
    await collection.create_index(["campaign_id", "code"], unique=True)
