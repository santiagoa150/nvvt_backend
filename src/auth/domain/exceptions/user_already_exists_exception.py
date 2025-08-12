from fastapi import status

from auth.domain.exceptions.user_exception_messages import UserExceptionMessages
from shared.domain.exceptions.common_exception import CommonException


class UserAlreadyExistsException(CommonException):
    """Exception raised when a user already exists in the system."""

    def __init__(self, message: str):
        super().__init__(status.HTTP_409_CONFLICT, message)

    @staticmethod
    def email_already_exists(email: str) -> "UserAlreadyExistsException":
        """Raises an exception when a user with the same email already exists."""
        return UserAlreadyExistsException(
            UserExceptionMessages.EMAIL_ALREADY_EXISTS.format(email=email)
        )
