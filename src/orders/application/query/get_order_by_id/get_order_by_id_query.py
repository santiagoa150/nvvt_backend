from shared.domain.cqrs.query.iquery import IQuery
from shared.domain.value_objects.id_value_object import IdValueObject


class GetOrderByIdQuery(IQuery):
    """Query to get an order by its ID."""

    def __init__(self, order_id: IdValueObject):
        """
        :param order_id: The ID of the order to retrieve.
        """
        self.order_id = order_id

    @staticmethod
    def create(order_id: str):
        """Factory method to create a GetOrderByIdQuery instance."""
        return GetOrderByIdQuery(
            IdValueObject(order_id, "order_id")
        )
