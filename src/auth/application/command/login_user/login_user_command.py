from shared.domain.cqrs.command.icommand import ICommand


class LoginUserCommand(ICommand):
    """Command to log in a user."""

    def __init__(self, email: str, password: str):
        """
        :param email: The email of the user.
        :param password: The password of the user.
        """
        self.email = email
        self.password = password
