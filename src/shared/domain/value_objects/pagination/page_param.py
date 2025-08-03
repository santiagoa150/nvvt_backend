from shared.domain.value_objects.int_value_object import IntValueObject


class PageParam(IntValueObject):
    """Value object representing a page parameter for pagination."""

    def __init__(self, value: int):
        """
        :param value: The page number, must be greater than 0.
        """
        super().__init__(value, field_name="page", min_value=1)
