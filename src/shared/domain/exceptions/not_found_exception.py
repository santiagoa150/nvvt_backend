from fastapi import status

from shared.domain.exceptions.common_exception import CommonException


class NotFoundException(CommonException):
    """Exception raised when a requested resource is not found."""

    def __init__(self, message: str):
        super().__init__(status.HTTP_404_NOT_FOUND, message)
