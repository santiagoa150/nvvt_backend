import re

from shared.domain.exceptions.str_value_object_exception import StrValueObjectException
from shared.domain.value_objects.str_value_object import StringValueObject


class Email(StringValueObject):
    """Represents an email address as a value object."""

    _REGEX = re.compile(
        r"^(?!.*\+)([A-Za-z0-9](?:[A-Za-z0-9._%\-]*[A-Za-z0-9])?)@([A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)*)\.[A-Za-z]{2,}$"
    )

    def __init__(self, value: str, field_name: str = "email"):
        """
        :param value: The email address as a string.
        :param field_name: The name of the field for error messages.
        """
        super().__init__(value, field_name)

    def _validate(self, value: str):
        """
        Validates that the provided value is a valid email address.

        :raises StringValueObjectException: If the value is not a valid email.
        """
        super()._validate(value)

        if self._REGEX.match(value) is None:
            raise StrValueObjectException.value_must_be_valid_email(value)
