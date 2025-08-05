from shared.domain.cqrs.query.iquery import IQuery
from shared.domain.value_objects.id_value_object import IdValueObject


class GetClientByIdQuery(IQuery):
    """Query to get a client by its ID."""

    def __init__(self, client_id: IdValueObject):
        """
        :param client_id: The ID of the client to retrieve.
        """
        self.client_id = client_id

    @staticmethod
    def create(client_id: str):
        """Factory method to create a GetClientByIdQuery instance."""
        return GetClientByIdQuery(
            client_id=IdValueObject(client_id, "client_id")
        )
