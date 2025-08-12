from shared.domain.exceptions.bool_value_object_exception import (
    BoolValueObjectException,
)


class BoolValueObject:

    def __init__(self, value: bool, field_name: str = "boolean"):
        """
        :param value: The boolean value.
        :param field_name: The name of the field for error messages.
        """
        self._field_name = field_name
        self._validate(value)
        self._value = value

    def _validate(self, value: bool):
        """
        Validates that the provided value is a boolean.

        :raises BoolValueObjectException: If the provided value is not a boolean.
        """
        if not isinstance(value, bool):
            raise BoolValueObjectException.value_must_be_boolean(self._field_name)

    @property
    def bool(self) -> bool:
        """Returns the value of the boolean value object."""
        return self._value
