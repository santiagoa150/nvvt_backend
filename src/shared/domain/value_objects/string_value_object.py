from shared.domain.exceptions.common_exception_messages import CommonExceptionMessages
from shared.domain.exceptions.string_value_object_exception import StringValueObjectException


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
            raise StringValueObjectException(
                CommonExceptionMessages.STRING_VALUE_OBJECT_MUST_BE_STRING.format(string=self._field_name)
            )
        if not value.strip():
            raise StringValueObjectException(
                CommonExceptionMessages.STRING_VALUE_OBJECT_CANNOT_BE_EMPTY.format(string=self._field_name)
            )

    @property
    def str(self) -> str:
        """Returns the value of the string value object."""
        return self._value
