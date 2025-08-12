from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt

from auth.domain.repository.token_repository import TokenRepository


class JwtTokenRepository(TokenRepository):
    """Implementation of the TokenRepository using JWT for token signing and verification."""

    async def sign(self, payload: dict, secret: str, exp_minutes: int) -> str:
        """Sign a payload to create a JWT token."""

        expires_in = datetime.now(timezone.utc) + timedelta(minutes=exp_minutes)
        to_encode = payload.copy()
        to_encode.update({"exp": expires_in})
        return jwt.encode(to_encode, secret, algorithm="HS256")

    async def verify(self, token: str, secret: str) -> Optional[dict]:
        """Verify a JWT token and return its payload if valid."""
        try:
            return jwt.decode(token, secret, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
