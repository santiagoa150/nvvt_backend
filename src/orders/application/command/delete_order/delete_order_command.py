from shared.domain.cqrs.command.icommand import ICommand
from shared.domain.value_objects.id_value_object import IdValueObject


class DeleteOrderCommand(ICommand):
    """Command to delete an order by its ID."""

    def __init__(self, order_id: IdValueObject):
        """
        :param order_id: The ID of the order to delete.
        """
        self.order_id = order_id

    @staticmethod
    def create(order_id: str) -> "DeleteOrderCommand":
        """Factory method to create a DeleteOrderCommand instance."""
        return DeleteOrderCommand(
            IdValueObject(order_id, "order_id"),
        )
