from shared.domain.cqrs.command.icommand import ICommand
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.positive_int_value_object import PositiveIntValueObject


class UpdateProductQuantityCommand(ICommand):
    """Command to update the quantity of a product."""

    def __init__(self, product_id: IdValueObject, quantity: PositiveIntValueObject):
        """
        :param product_id: The ID of the product to update.
        :param quantity: The new quantity for the product.
        """
        self.product_id = product_id
        self.quantity = quantity

    @staticmethod
    def create(product_id: str, quantity: int) -> "UpdateProductQuantityCommand":
        """Factory method to create an UpdateProductQuantityCommand instance."""
        return UpdateProductQuantityCommand(
            product_id=IdValueObject(product_id, "product_id"),
            quantity=PositiveIntValueObject(quantity, "product_quantity"),
        )
