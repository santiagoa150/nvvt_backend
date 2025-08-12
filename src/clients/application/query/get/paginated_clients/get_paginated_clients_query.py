from shared.domain.cqrs.query.iquery import IQuery
from shared.domain.value_objects.pagination.limit_param import LimitParam
from shared.domain.value_objects.pagination.page_param import PageParam


class GetPaginatedClientsQuery(IQuery):
    """Query to get paginated clients."""

    def __init__(self, page: PageParam, limit: LimitParam):
        """
        :param page: The page number to retrieve.
        :param limit: The number of items per page.
        """
        self.page = page
        self.limit = limit

    @staticmethod
    def create(page: int, limit: int | float):
        """Factory method to create a GetPaginatedClientsQuery instance."""
        return GetPaginatedClientsQuery(page=PageParam(page), limit=LimitParam(float(limit)))
