from fastapi import APIRouter, Depends, Query

from clients.application.query.get_client_by_id.get_client_by_id_query import GetClientByIdQuery
from clients.application.query.get_paginated_clients.get_paginated_clients_query import GetPaginatedClientsQuery
from clients.domain.client import Client
from shared import get_query_bus
from shared.domain.cqrs.query.query_bus import QueryBus
from shared.domain.pagination_dict import PaginationDict
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.pagination.limit_param import LimitParam
from shared.domain.value_objects.pagination.page_param import PageParam

router = APIRouter()


@router.get('/')
async def get_paginated_clients(
        page: int = Query(1, description='Page number to retrieve'),
        limit: int = Query(20, description='Number of items per page'),
        query_bus: QueryBus = Depends(get_query_bus)
):
    """Retrieve paginated clients."""
    pagination = await query_bus.query(GetPaginatedClientsQuery(
        PageParam(page),
        LimitParam(float(limit)),
    ))
    return PaginationDict(
        data=[client.to_dict() for client in pagination['data']],
        metadata=pagination['metadata'],
    )


@router.get('/{client_id}')
async def get_client_by_id(client_id: str, query_bus: QueryBus = Depends(get_query_bus)):
    """Retrieve a client by its ID."""
    client: Client = await query_bus.query(GetClientByIdQuery(
        IdValueObject(client_id, 'client_id')
    ))
    return client.to_dict()
