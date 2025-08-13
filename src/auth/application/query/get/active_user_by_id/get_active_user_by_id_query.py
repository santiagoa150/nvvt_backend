from shared.domain.cqrs.query.iquery import IQuery
from shared.domain.value_objects.id_value_object import IdValueObject


class GetActiveUserByIdQuery(IQuery):
    """
    Query to get an active user by their ID.
    """

    def __init__(self, user_id: IdValueObject):
        """
        Initializes the GetActiveUserByIdQuery with the user's ID.

        :param user_id: The ID of the user to retrieve.
        """
        self.user_id = user_id

    @staticmethod
    def create(user_id: str) -> "GetActiveUserByIdQuery":
        """Factory method to create a GetActiveUserByIdQuery from a string user ID."""
        return GetActiveUserByIdQuery(IdValueObject(user_id, "user_id"))
