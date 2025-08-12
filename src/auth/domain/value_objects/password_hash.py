import hashlib
import re

from auth.domain.exceptions.password_exception import PasswordException
from auth.domain.value_objects.password import Password
from shared.domain.value_objects.str_value_object import StringValueObject


class PasswordHash(StringValueObject):
    """Value object representing a password hash."""

    _REGEX = re.compile(r"^[a-fA-F0-9]{64}$")

    def __init__(self, value: str, field_name: str = "password_hash"):
        """
        :param value: The password hash as a string.
        :param field_name: The name of the field for error messages.
        """
        super().__init__(value, field_name)

    def _validate(self, value: str):
        """
        Validates that the provided value is a valid password hash.
        """
        super()._validate(value)

        if self._REGEX.match(value) is None:
            raise PasswordException.invalid_password_hash()

    def compare(self, password: Password) -> bool:
        """
        Compares the password hash with a Password value object.
        :param password: The Password value object to compare against.
        :return: True if the password matches the hash, False otherwise.
        """
        return self.str == PasswordHash.create_from(password).str

    @staticmethod
    def create_from(password: Password) -> "PasswordHash":
        """
        Creates a PasswordHash from a Password value object.
        :param password: The Password value object.
        :return: A PasswordHash value object.
        """

        return PasswordHash(hashlib.sha256(password.str.encode("utf-8")).hexdigest())
