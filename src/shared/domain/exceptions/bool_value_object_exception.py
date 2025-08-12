from fastapi import status

from shared.domain.exceptions.common_exception import CommonException
from shared.domain.exceptions.common_exception_messages import CommonExceptionMessages


class BoolValueObjectException(CommonException):
    """Exception raised for errors in the BoolValueObject."""

    def __init__(self, message: str):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)

    @staticmethod
    def value_must_be_boolean(value: str) -> "BoolValueObjectException":
        """Raises an exception when the value is not a boolean."""
        return BoolValueObjectException(
            CommonExceptionMessages.BOOLEAN_VALUE_OBJECT_MUST_BE_BOOLEAN.format(value=value)
        )
