from fastapi import status

from shared.domain.exceptions.common_exception import CommonException


class IntValueObjectException(CommonException):
    """Exception raised for errors in integer value objects."""

    def __init__(self, message: str):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)
