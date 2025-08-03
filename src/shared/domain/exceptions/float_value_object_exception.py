from fastapi import status

from shared.domain.exceptions.common_exception import CommonException
from shared.domain.exceptions.common_exception_messages import CommonExceptionMessages


class FloatValueObjectException(CommonException):
    """Exception raised for errors in float value objects."""

    def __init__(self, message: str):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)

    @staticmethod
    def value_must_be_float(field_name: str) -> "FloatValueObjectException":
        """Raises an exception when the value is not a float."""
        return FloatValueObjectException(
            CommonExceptionMessages.FLOAT_VALUE_OBJECT_MUST_BE_FLOAT.format(float=field_name)
        )

    @staticmethod
    def min_value_exceeded(field_name: str, min_value: float) -> "FloatValueObjectException":
        """Raises an exception when the value is less than the minimum allowed."""
        return FloatValueObjectException(
            CommonExceptionMessages.FLOAT_VALUE_OBJECT_MIN_VALUE.format(float=field_name, min_value=min_value)
        )

    @staticmethod
    def max_value_exceeded(field_name: str, max_value: float) -> "FloatValueObjectException":
        """Raises an exception when the value is greater than the maximum allowed."""
        return FloatValueObjectException(
            CommonExceptionMessages.FLOAT_VALUE_OBJECT_MAX_VALUE.format(float=field_name, max_value=max_value)
        )
