from typing import Optional, cast

from motor.motor_asyncio import AsyncIOMotorCollection

from auth.domain.repository.user_read_repository import UserReadRepository
from auth.domain.user import User
from auth.domain.user_dict import UserDict
from shared.domain.value_objects.common.email import Email


class MongoDBUserReadRepository(UserReadRepository):
    """MongoDB implementation of the UserReadRepository interface for reading user data."""

    def __init__(self, collection: AsyncIOMotorCollection):
        """Initializes the MongoDBUserReadRepository with a MongoDB collection."""
        self._collection = collection

    async def get_user_by_email(self, email: Email) -> Optional[User]:
        """Retrieve a user by their email address."""
        document = await self._collection.find_one({"email": email.str})

        if document is None:
            return None

        return User.from_dict(cast(UserDict, document))
