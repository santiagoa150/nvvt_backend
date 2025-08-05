from shared.domain.value_objects.int_value_object import IntValueObject


class PositiveIntValueObject(IntValueObject):
    """Value object representing a positive integer."""

    def __init__(self, value: int, field_name: str = "positive integer"):
        super().__init__(value, field_name, min_value=1)
