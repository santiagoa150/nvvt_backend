from fastapi import status

from shared.domain.exceptions.common_exception import CommonException
from shared.domain.exceptions.common_exception_messages import CommonExceptionMessages


class PhoneValueObjectException(CommonException):
    """Exception raised for errors in phone value objects."""

    def __init__(self, message: str):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)

    @staticmethod
    def phone_must_be_dict(number) -> "PhoneValueObjectException":
        """Raises an exception when the phone value is not a dictionary."""
        return PhoneValueObjectException(
            CommonExceptionMessages.PHONE_NUMBER_MUST_BE_VALID.format(number=number)
        )
