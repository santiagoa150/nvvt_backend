from shared.domain.cqrs.query.iquery import IQuery


class VerifyUserAccessTokenQuery(IQuery):
    """Query to verify a user's access token."""

    def __init__(self, access_token: str):
        """
        :param access_token: The access token to verify.
        """
        self.access_token = access_token
