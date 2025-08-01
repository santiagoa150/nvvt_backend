from fastapi import status
from shared.domain.exceptions.common_exception import CommonException


class CqrsException(CommonException):
    """Base class for all CQRS-related exceptions."""

    def __init__(self, message: str):
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, message)
