from shared.domain.exceptions.float_value_object_exception import FloatValueObjectException


class FloatValueObject:
    """A value object that represents a float with optional constraints."""

    def __init__(
            self,
            value: float,
            field_name: str = "float",
            *,
            min_value: float | None = None,
            max_value: float | None = None,
    ):
        self._field_name = field_name
        self._min_value = min_value
        self._max_value = max_value
        self._validate(value)
        self._value = value

    def _validate(self, value: float):

        if not isinstance(value, float):
            raise FloatValueObjectException.value_must_be_float(self._field_name)

        if self._min_value is not None and value < self._min_value:
            raise FloatValueObjectException.min_value_exceeded(self._field_name, self._min_value)

        if self._max_value is not None and value > self._max_value:
            raise FloatValueObjectException.max_value_exceeded(self._field_name, self._max_value)

    @property
    def float(self) -> float:
        """Returns the value of the float value object."""
        return self._value
