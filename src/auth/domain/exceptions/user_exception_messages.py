from enum import Enum


class UserExceptionMessages(str, Enum):
    """Class containing exception messages for user domain exceptions."""

    PASSWORD_TOO_WEAK = "Password is too weak. It must contain at least 8 characters, including uppercase, lowercase, numbers, and special characters."
    INVALID_PASSWORD_HASH = "Invalid password hash. It must be a 64-character hexadecimal string."
    EMAIL_ALREADY_EXISTS = "User with email '{email}' already exists."

    def format(self, **kwargs) -> str:
        """Format the message with the provided keyword arguments."""
        return self.value.format(**kwargs)
