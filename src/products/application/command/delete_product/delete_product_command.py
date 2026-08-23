from shared.domain.cqrs.command.icommand import ICommand
from shared.domain.value_objects.id_value_object import IdValueObject


class DeleteProductCommand(ICommand):
    """Command to delete a product by its ID."""

    def __init__(self, product_id: IdValueObject):
        """
        :param product_id: The ID of the product to delete.
        """
        self.product_id = product_id

    @staticmethod
    def create(product_id: str) -> "DeleteProductCommand":
        """Factory method to create a DeleteProductCommand instance."""
        return DeleteProductCommand(product_id=IdValueObject(product_id, "product_id"))
