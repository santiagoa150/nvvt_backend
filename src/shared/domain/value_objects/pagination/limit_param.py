from shared.domain.value_objects.float_value_object import FloatValueObject


class LimitParam(FloatValueObject):
    """Value object representing a limit parameter for pagination."""

    def __init__(self, value: float):
        """
        :param value: The limit value, must be greater than 0.
        """
        super().__init__(value, field_name="limit", min_value=1)
