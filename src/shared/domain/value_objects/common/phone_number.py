from shared.domain.exceptions.phone_value_object_exception import PhoneValueObjectException
from shared.domain.value_objects.str_value_object import StringValueObject


class PhoneNumber(StringValueObject):
    """Represents a phone number as an integer value object."""

    def __init__(self, value: str, field_name: str = "phone_number"):
        """
        :param value: The phone number integer value as a string.
        :param field_name: The name of the field for error messages.
        """
        super().__init__(value, field_name)

    def _validate(self, value: str):
        """
        Validates that the provided value is a string representing a phone number.
        Raises:
            ValueError: If the value is not a string or does not match the phone number format.
        """
        super()._validate(value)
        try:
            int(value)
        except ValueError:
            raise PhoneValueObjectException.phone_must_be_dict(value)

        if len(value) < 7 or len(value) > 12:
            raise PhoneValueObjectException.phone_must_be_dict(value)
