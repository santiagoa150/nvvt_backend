from shared.domain.exceptions.int_value_object_exception import IntValueObjectException


class IntValueObject:
    """Base class for integer value objects."""

    def __init__(
        self,
        value: int,
        field_name: str = "integer",
        *,
        min_value: int | None = None,
        max_value: int | None = None,
    ):
        self._field_name = field_name
        self._min_value = min_value
        self._max_value = max_value
        self._validate(value)
        self._value = value

    def _validate(self, value: int):
        """
        Validates that the provided value is an integer and within the specified range.
        Raises:
            IntValueObjectException: If the value is not an integer,
            or if it is outside the specified range.
        """

        if not isinstance(value, int):
            raise IntValueObjectException.value_must_be_integer(self._field_name)

        if self._min_value is not None and value < self._min_value:
            raise IntValueObjectException.min_value_exceeded(self._field_name, self._min_value)

        if self._max_value is not None and value > self._max_value:
            raise IntValueObjectException.max_value_exceeded(self._field_name, self._max_value)

    @property
    def int(self) -> int:
        """Returns the value of the integer value object."""
        return self._value
