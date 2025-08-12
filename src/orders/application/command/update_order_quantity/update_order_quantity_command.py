from shared.domain.cqrs.command.icommand import ICommand
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.positive_int_value_object import PositiveIntValueObject


class UpdateOrderQuantityCommand(ICommand):
    """Command to update the quantity of an existing order."""

    def __init__(self, order_id: IdValueObject, quantity: PositiveIntValueObject):
        """
        :param order_id: The ID of the order to update.
        :param quantity: The new quantity for the order.
        """
        self.order_id = order_id
        self.quantity = quantity

    @staticmethod
    def create(order_id: str, quantity: int):
        """Factory method to create an UpdateOrderQuantityCommand instance."""
        return UpdateOrderQuantityCommand(
            order_id=IdValueObject(order_id, "order_id"),
            quantity=PositiveIntValueObject(quantity, "order_quantity"),
        )
