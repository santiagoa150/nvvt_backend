import uuid

from shared.domain.exceptions.common_exception_messages import CommonExceptionMessages
from shared.domain.exceptions.string_value_object_exception import StringValueObjectException
from shared.domain.value_objects.string_value_object import StringValueObject


class IdValueObject(StringValueObject):
    """Base class for ID value objects, which are typically UUIDs or similar identifiers."""

    def __init__(self, value: str, field_name: str = "id") -> None:
        super().__init__(value, field_name)

    def _validate(self, value: str):
        """
        Validates that the provided value is a valid UUID string.
        Raises:
            StringValueObjectException: If the value is not a valid UUID.
        """
        super()._validate(value)

        try:
            uuid.UUID(value)
        except ValueError:
            raise StringValueObjectException(
                CommonExceptionMessages.ID_VALUE_OBJECT_MUST_BE_VALID_UUID.format(id=value)
            )
