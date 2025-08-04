from shared.domain.value_objects.int_value_object import IntValueObject


class PhoneNumber(IntValueObject):
    """Represents a phone number as an integer value object."""

    def __init__(self, value: int, field_name: str = "phone_number"):
        """
        :param value: The phone number as an integer.
        :param field_name: The name of the field for error messages.
        """
        super().__init__(value, field_name, min_value=1000000, max_value=999999999999)
