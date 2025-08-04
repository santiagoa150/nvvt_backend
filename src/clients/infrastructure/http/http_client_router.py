from fastapi import APIRouter, Depends

from clients.application.query.get_client_by_id.get_client_by_id_query import GetClientByIdQuery
from clients.domain.client import Client
from shared import get_query_bus
from shared.domain.cqrs.query.query_bus import QueryBus
from shared.domain.value_objects.id_value_object import IdValueObject

router = APIRouter()


@router.get('/{client_id}')
async def get_client_by_id(client_id: str, query_bus: QueryBus = Depends(get_query_bus)):
    """Retrieve a client by its ID."""
    client: Client = await query_bus.query(GetClientByIdQuery(
        IdValueObject(client_id)
    ))
    return client.to_dict()
