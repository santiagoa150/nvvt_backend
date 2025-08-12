from fastapi import status

from shared.domain.exceptions.common_exception import CommonException
from shared.domain.exceptions.common_exception_messages import CommonExceptionMessages


class StrValueObjectException(CommonException):
    """Exception raised for errors in string value objects."""

    def __init__(self, message: str):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)

    @staticmethod
    def value_must_be_string(field_name: str) -> "StrValueObjectException":
        """Raises an exception when the value is not a string."""
        return StrValueObjectException(
            CommonExceptionMessages.STRING_VALUE_OBJECT_MUST_BE_STRING.format(string=field_name)
        )

    @staticmethod
    def value_cannot_be_empty(field_name: str) -> "StrValueObjectException":
        """Raises an exception when the value is an empty string."""
        return StrValueObjectException(
            CommonExceptionMessages.STRING_VALUE_OBJECT_CANNOT_BE_EMPTY.format(string=field_name)
        )

    @staticmethod
    def value_must_be_and_id(value: str) -> "StrValueObjectException":
        """Raises an exception when the value is not a valid ID."""
        return StrValueObjectException(
            CommonExceptionMessages.ID_VALUE_OBJECT_MUST_BE_VALID_UUID.format(id=value)
        )

    @staticmethod
    def value_must_be_valid_email(value: str) -> "StrValueObjectException":
        """Raises an exception when the value is not a valid email."""
        return StrValueObjectException(
            CommonExceptionMessages.EMAIL_VALUE_OBJECT_MUST_BE_VALID_EMAIL.format(email=value)
        )
