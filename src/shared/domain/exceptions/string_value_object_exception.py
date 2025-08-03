from fastapi import status

from shared.domain.exceptions.common_exception import CommonException


class StringValueObjectException(CommonException):
    """Exception raised for errors in string value objects."""

    def __init__(self, message: str):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)
