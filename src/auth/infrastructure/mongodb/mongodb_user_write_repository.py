from motor.motor_asyncio import AsyncIOMotorCollection

from auth.domain.repository.user_write_repository import UserWriteRepository
from auth.domain.user import User


class MongoDBUserWriteRepository(UserWriteRepository):
    """MongoDB implementation of the UserWriteRepository interface for writing user data."""

    def __init__(self, collection: AsyncIOMotorCollection):
        """Initializes the MongoDBUserWriteRepository with a MongoDB collection."""
        self._collection = collection

    async def create_user(self, user: User) -> None:
        """Create a new user."""
        await self._collection.insert_one(user.to_dict())
