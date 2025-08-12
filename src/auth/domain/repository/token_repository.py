from abc import ABC, abstractmethod
from typing import Optional


class TokenRepository(ABC):
    """Abstract base class for token repository operations."""

    @abstractmethod
    async def sign(self, payload: dict, secret: str, exp_minutes: int) -> str:
        """
        Sign a payload to create a token.

        :param payload: The payload to sign.
        :param secret: The secret key used for signing.
        :param exp_minutes: The expiration time in minutes.
        :return: The signed token as a string.
        """
        pass

    @abstractmethod
    async def verify(self, token: str, secret: str) -> Optional[dict]:
        """
        Verify a token and return its payload.

        :param token: The token to verify.
        :param secret: The secret key used for verification.
        :return: The payload contained in the token if valid, otherwise None.
        """
        pass
