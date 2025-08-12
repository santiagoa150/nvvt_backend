from abc import ABC, abstractmethod

from auth.domain.user import User


class UserWriteRepository(ABC):
    """Abstract base class for user writing repository operations."""

    @abstractmethod
    async def create_user(self, user: User) -> None:
        """
        Create a new user.

        :param user: The user object to create.
        """
        pass
