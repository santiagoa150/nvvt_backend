from fastapi import status

from auth.domain.exceptions.user_exception_messages import UserExceptionMessages
from shared.domain.exceptions.common_exception import CommonException


class PasswordException(CommonException):
    """Base exception for user password errors."""

    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code, message)

    @staticmethod
    def password_too_weak() -> "PasswordException":
        """Raises an exception when the password is too weak."""
        return PasswordException(UserExceptionMessages.PASSWORD_TOO_WEAK.value)

    @staticmethod
    def invalid_password_hash() -> "PasswordException":
        """Raises an exception when the password hash is invalid."""
        return PasswordException(UserExceptionMessages.INVALID_PASSWORD_HASH.value)
