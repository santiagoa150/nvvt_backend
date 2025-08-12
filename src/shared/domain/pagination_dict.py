from typing import Generic, TypedDict, TypeVar

T = TypeVar("T")


class MetadataDict(TypedDict):
    """Dictionary representation of pagination metadata."""

    total: int
    total_pages: int
    page: int


class PaginationDict(Generic[T], TypedDict):
    """Dictionary representation of paginated data."""

    data: list[T]
    metadata: MetadataDict


def empty_pagination_dict() -> PaginationDict:
    """Return an empty PaginationDict."""
    return PaginationDict(data=[], metadata={"total": 0, "total_pages": 0, "page": 1})
