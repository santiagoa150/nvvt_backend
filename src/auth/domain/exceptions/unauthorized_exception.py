from fastapi import status

from auth.domain.exceptions.user_exception_messages import UserExceptionMessages
from shared.domain.exceptions.common_exception import CommonException


class UnauthorizedException(CommonException):
    """Exception raised when a user is not authorized to perform an action."""

    def __init__(self, message: str):
        super().__init__(status.HTTP_401_UNAUTHORIZED, message)

    @staticmethod
    def user_not_authenticated() -> "UnauthorizedException":
        """Raises an exception when the user is not authenticated."""
        return UnauthorizedException(UserExceptionMessages.USER_NOT_AUTHENTICATED.value)

    @staticmethod
    def invalid_refresh_token() -> "UnauthorizedException":
        """Raises an exception when the refresh token is invalid."""
        return UnauthorizedException(UserExceptionMessages.INVALID_REFRESH_TOKEN.value)
