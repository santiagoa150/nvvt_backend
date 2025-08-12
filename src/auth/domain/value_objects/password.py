import re

from auth.domain.exceptions.password_exception import PasswordException
from shared.domain.value_objects.str_value_object import StringValueObject


class Password(StringValueObject):
    """Value object representing a password."""

    _REGEX = re.compile(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{8,}$'
    )

    def __init__(self, value: str, field_name: str = "password"):
        """
        :param value: The password as a string.
        :param field_name: The name of the field for error messages.
        """
        super().__init__(value, field_name)

    def _validate(self, value: str):
        """
        Validates that the provided value is a valid password.

        :raises UserPasswordException: Raises an exception when the password is too weak.
        """
        super()._validate(value)

        if self._REGEX.match(value) is None:
            raise PasswordException.password_too_weak()
