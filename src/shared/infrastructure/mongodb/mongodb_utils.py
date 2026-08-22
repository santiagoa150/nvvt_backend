from shared.domain.value_objects.pagination.limit_param import LimitParam
from shared.domain.value_objects.pagination.page_param import PageParam


class MongoDBUtils:
    """Utility class for MongoDB operations, particularly for building paginated queries."""

    @staticmethod
    def build_paginated_query(
        page: PageParam, limit: LimitParam, sort: dict[str, int] | None = None
    ) -> list[dict]:
        """
        Build a paginated query for MongoDB.
        :param page: The page number to retrieve.
        :param limit: The number of items per page.
        :param sort: The sort specification to apply before paginating. Defaults to newest first.
        :return: A dictionary representing the paginated query.
        """
        skip: float = (page.int - 1) * limit.float
        sort = sort if sort is not None else {"_id": -1}
        return [
            {
                "$facet": {
                    "data": [{"$sort": sort}, {"$skip": skip}, {"$limit": limit.float}],
                    "metadata": [
                        {"$count": "total"},
                        {
                            "$addFields": {
                                "total_pages": {"$ceil": {"$divide": ["$total", limit.float]}},
                                "page": page.int,
                            }
                        },
                    ],
                }
            }
        ]
