from motor.motor_asyncio import AsyncIOMotorCollection

from campaigns.domain.campaign_status import CampaignStatus


async def create_campaign_indexes(collection: AsyncIOMotorCollection) -> None:
    """Creates indexes for the campaigns collection."""
    await collection.create_index("campaign_id", unique=True)
    await collection.create_index(["year", "number"], unique=True)
    await collection.create_index(
        "status",
        unique=True,
        partialFilterExpression={"status": CampaignStatus.ACTIVE.value},
    )
    # Supports the paginated listing's status-priority sort (see
    # MongoDBCampaignReadRepository), then year and number descending.
    await collection.create_index(["status", "year", "number"])
