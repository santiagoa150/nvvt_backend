from shared.domain.exceptions.str_value_object_exception import StrValueObjectException


class StringValueObject:
    """Base class for string value objects."""

    def __init__(self, value: str, field_name: str = "string"):
        self._field_name = field_name
        self._validate(value)
        self._value = value

    def _validate(self, value: str):
        """
        Validates that the provided value is a non-empty string.
        Raises:
            StringValueObjectException: If the value is not a string or is empty.
        """
        if not isinstance(value, str):
            raise StrValueObjectException.value_must_be_string(self._field_name)
        if not value.strip():
            raise StrValueObjectException.value_cannot_be_empty(self._field_name)

    @property
    def str(self) -> str:
        """Returns the value of the string value object."""
        return self._value
