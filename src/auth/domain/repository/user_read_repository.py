from abc import ABC, abstractmethod
from typing import Optional

from auth.domain.user import User
from shared.domain.value_objects.common.email import Email


class UserReadRepository(ABC):
    """Abstract base class for user reading repository operations."""

    @abstractmethod
    async def get_user_by_email(self, email: Email) -> Optional[User]:
        """
        Retrieve a user by their email address.

        :param email: The email of the user to retrieve.
        :return: An instance of User if found, otherwise None.
        """
        pass
