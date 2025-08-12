from auth.domain.value_objects.password import Password
from shared.domain.cqrs.command.icommand import ICommand
from shared.domain.value_objects.common.email import Email


class CreateUserCommand(ICommand):
    """Command to create a new user."""

    def __init__(
            self,
            email: Email,
            password: Password,
    ):
        """
        :param email: The email of the user.
        :param password: The password of the user.
        """
        self.email = email
        self.password = password

    @staticmethod
    def create(
            email: str,
            password: str,
    ):
        """Factory method to create a CreateUserCommand instance."""
        return CreateUserCommand(
            email=Email(email, "user_email"),
            password=Password(password, "user_password"),
        )
