from shared.domain.cqrs.query.iquery import IQuery
from shared.domain.value_objects.pagination.limit_param import LimitParam
from shared.domain.value_objects.pagination.page_param import PageParam
from shared.domain.value_objects.str_value_object import StringValueObject


class GetPaginatedNotificationsQuery(IQuery):
    """Query to get paginated notifications for a recipient."""

    def __init__(self, recipient: StringValueObject, page: PageParam, limit: LimitParam):
        """
        :param recipient: The ID of the recipient to retrieve notifications for.
        :param page: The page number to retrieve.
        :param limit: The number of items per page.
        """
        self.recipient = recipient
        self.page = page
        self.limit = limit

    @staticmethod
    def create(recipient: str, page: int, limit: int | float) -> "GetPaginatedNotificationsQuery":
        """Factory method to create a GetPaginatedNotificationsQuery instance."""
        return GetPaginatedNotificationsQuery(
            recipient=StringValueObject(recipient, "notification_recipient"),
            page=PageParam(page),
            limit=LimitParam(float(limit)),
        )
