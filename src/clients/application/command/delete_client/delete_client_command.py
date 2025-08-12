from shared.domain.cqrs.command.icommand import ICommand
from shared.domain.value_objects.id_value_object import IdValueObject


class DeleteClientCommand(ICommand):
    """Command to delete a client by its ID."""

    def __init__(self, client_id: IdValueObject):
        """
        :param client_id: The ID of the client to delete.
        """
        self.client_id = client_id

    @staticmethod
    def create(client_id: str):
        """Factory method to create a DeleteClientCommand instance."""
        return DeleteClientCommand(client_id=IdValueObject(client_id, "client_id"))
