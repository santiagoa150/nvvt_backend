from shared.domain.value_objects.int_value_object import IntValueObject


class CountryPhoneCode(IntValueObject):
    """Represents a country phone code as an integer value object."""

    def __init__(self, value: int, field_name: str = "country_phone_code"):
        """
        :param value: The country phone code as an integer.
        :param field_name: The name of the field for error messages.
        """
        super().__init__(value, field_name, min_value=1, max_value=998)
