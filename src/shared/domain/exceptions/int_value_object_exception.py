from fastapi import status

from shared.domain.exceptions.common_exception import CommonException
from shared.domain.exceptions.common_exception_messages import CommonExceptionMessages


class IntValueObjectException(CommonException):
    """Exception raised for errors in integer value objects."""

    def __init__(self, message: str):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)

    @staticmethod
    def value_must_be_integer(field_name: str) -> "IntValueObjectException":
        """Raises an exception when the value is not an integer."""
        return IntValueObjectException(
            CommonExceptionMessages.INT_VALUE_OBJECT_MUST_BE_INTEGER.format(integer=field_name)
        )

    @staticmethod
    def min_value_exceeded(field_name: str, min_value: int) -> "IntValueObjectException":
        """Raises an exception when the value is less than the minimum allowed."""
        return IntValueObjectException(
            CommonExceptionMessages.INT_VALUE_OBJECT_MIN_VALUE.format(integer=field_name, min_value=min_value)
        )

    @staticmethod
    def max_value_exceeded(field_name: str, max_value: int) -> "IntValueObjectException":
        """Raises an exception when the value is greater than the maximum allowed."""
        return IntValueObjectException(
            CommonExceptionMessages.INT_VALUE_OBJECT_MAX_VALUE.format(integer=field_name, max_value=max_value)
        )
