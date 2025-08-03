from datetime import datetime

from shared.domain.value_objects.int_value_object import IntValueObject


class Year(IntValueObject):
    """Value object representing a year."""

    def __init__(self, value: int, field_name: str = "year"):
        super().__init__(value, field_name, min_value=1900, max_value=Year.current_year() + 10)

    @staticmethod
    def current_year() -> int:
        """Returns the current year."""
        return datetime.now().year
