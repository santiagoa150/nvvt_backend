from shared.domain.value_objects.float_value_object import FloatValueObject


class PositiveFloatValueObject(FloatValueObject):
    """Value object representing a positive float."""

    def __init__(self, value: float, field_name: str = "positive float"):
        super().__init__(value, field_name, min_value=1.0)
