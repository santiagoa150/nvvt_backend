from shared.domain.cqrs.command.icommand import ICommand


class RefreshUserAuthTokensCommand(ICommand):
    """Command to refresh user authentication tokens."""

    def __init__(self, refresh_token: str):
        """
        :param refresh_token: The refresh token of the user.
        """
        self.refresh_token = refresh_token
