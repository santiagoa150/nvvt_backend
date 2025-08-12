from fastapi import status

from shared.domain.exceptions.common_exception import CommonException
from shared.domain.exceptions.common_exception_messages import CommonExceptionMessages


class NotFoundException(CommonException):
    """Exception raised when a requested resource is not found."""

    def __init__(self, message: str):
        super().__init__(status.HTTP_404_NOT_FOUND, message)

    @staticmethod
    def entity_not_found(entity: str, entity_id: str) -> "NotFoundException":
        """Create a NotFoundException for a specific entity and ID."""
        return NotFoundException(
            CommonExceptionMessages.ENTITY_NOT_FOUND.format(entity=entity, id=entity_id)
        )
