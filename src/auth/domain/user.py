from auth.domain.user_dict import UserDict
from auth.domain.value_objects.password_hash import PasswordHash
from shared.domain.value_objects.bool_value_object import BoolValueObject
from shared.domain.value_objects.common.email import Email
from shared.domain.value_objects.id_value_object import IdValueObject


class User:
    """Represents a user in the system."""

    __slots__ = ("_user_id", "_email", "_password", "_is_active")

    def __init__(
        self,
        user_id: IdValueObject,
        email: Email,
        password: PasswordHash,
        is_active: BoolValueObject,
    ):
        self._user_id = user_id
        self._email = email
        self._password = password
        self._is_active = is_active

    def to_dict(self) -> UserDict:
        """Convert the User object to a dictionary representation."""
        return UserDict(
            user_id=self._user_id.str,
            email=self._email.str,
            password=self._password.str,
            is_active=self._is_active.bool,
        )

    @property
    def user_id(self) -> IdValueObject:
        return self._user_id

    @property
    def email(self) -> Email:
        return self._email

    @property
    def password(self) -> PasswordHash:
        return self._password

    @classmethod
    def from_dict(cls, user_dict: UserDict) -> "User":
        """Create a User object from a dictionary representation."""
        return cls(
            user_id=IdValueObject(user_dict["user_id"], "user_id"),
            email=Email(user_dict["email"], "user_email"),
            password=PasswordHash(user_dict["password"], "user_password"),
            is_active=BoolValueObject(user_dict["is_active"], "user_is_active"),
        )
