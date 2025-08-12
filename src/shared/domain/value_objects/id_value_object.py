import uuid

from shared.domain.exceptions.str_value_object_exception import StrValueObjectException
from shared.domain.value_objects.str_value_object import StringValueObject


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
            raise StrValueObjectException.value_must_be_and_id(value)

    @staticmethod
    def generate() -> str:
        """
        Generates a new UUID string.
        Returns:
            str: A new UUID string.
        """
        return str(uuid.uuid4())
