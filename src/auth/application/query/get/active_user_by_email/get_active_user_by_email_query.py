from shared.domain.cqrs.query.iquery import IQuery
from shared.domain.value_objects.common.email import Email


class GetActiveUserByEmailQuery(IQuery):
    """Query to get an active user by their email address."""

    def __init__(self, email: Email):
        """
        :param email: The email of the user to retrieve.
        """
        self.email = email

    @staticmethod
    def create(email: str) -> "GetActiveUserByEmailQuery":
        """Factory method to create a GetActiveUserByEmailQuery from a string email."""
        return GetActiveUserByEmailQuery(Email(email, "user_email"))
