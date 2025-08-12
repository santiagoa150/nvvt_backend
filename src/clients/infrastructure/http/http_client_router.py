from fastapi import APIRouter, Depends, Query, Body
from fastapi.security import HTTPBearer

from clients.application.command.create_client.create_client_command import CreateClientCommand
from clients.application.command.delete_client.delete_client_command import DeleteClientCommand
from clients.application.command.update_client.update_client_command import UpdateClientCommand
from clients.application.query.get.client_by_id.get_client_by_id_query import GetClientByIdQuery
from clients.application.query.get.paginated_clients.get_paginated_clients_query import GetPaginatedClientsQuery
from clients.domain.client import Client
from shared import get_query_bus, get_command_bus
from shared.domain.cqrs.command.command_bus import CommandBus
from shared.domain.cqrs.query.query_bus import QueryBus
from shared.domain.pagination_dict import PaginationDict
from shared.infrastructure.jwt.jwt_guard import jwt_guard

router = APIRouter()
bearer_scheme = HTTPBearer()


@router.get('/', dependencies=[Depends(bearer_scheme), Depends(jwt_guard)])
async def get_paginated_clients(
        page: int = Query(1, description='Page number to retrieve'),
        limit: int = Query(20, description='Number of items per page'),
        query_bus: QueryBus = Depends(get_query_bus)
):
    """Retrieve paginated clients."""
    pagination = await query_bus.query(GetPaginatedClientsQuery.create(page, limit))
    return PaginationDict(
        data=[client.to_dict() for client in pagination['data']],
        metadata=pagination['metadata'],
    )


@router.post('/', dependencies=[Depends(bearer_scheme), Depends(jwt_guard)])
async def create_client(
        given_names: str = Body(..., description='Given names of the client'),
        family_names: str = Body(None, description='Family names of the client'),
        delivery_place: str = Body(..., description='Delivery place of the client'),
        phone_number: str = Body(None, description='Phone number of the client'),
        country_phone_code: int = Body(None, description='Country phone code of the client'),
        command_bus: CommandBus = Depends(get_command_bus)
):
    """Create a new client."""
    await command_bus.dispatch(CreateClientCommand.create(
        given_names=given_names,
        family_names=family_names,
        delivery_place=delivery_place,
        phone_number=phone_number,
        country_phone_code=country_phone_code
    ))
    return {}


@router.get('/{client_id}', dependencies=[Depends(bearer_scheme), Depends(jwt_guard)])
async def get_client_by_id(client_id: str, query_bus: QueryBus = Depends(get_query_bus)):
    """Retrieve a client by its ID."""
    client: Client = await query_bus.query(GetClientByIdQuery.create(client_id))
    return client.to_dict()


@router.patch('/{client_id}', dependencies=[Depends(bearer_scheme), Depends(jwt_guard)])
async def update_client_by_id(
        client_id: str,
        given_names: str = Body(None, description='Given names of the client'),
        family_names: str = Body(None, description='Family names of the client'),
        delivery_place: str = Body(None, description='Delivery place of the client'),
        phone_number: str = Body(None, description='Phone number of the client'),
        country_phone_code: int = Body(None, description='Country phone code of the client'),
        command_bus: CommandBus = Depends(get_command_bus)
):
    """Update a client by its ID."""
    await command_bus.dispatch(UpdateClientCommand.create(
        client_id=client_id,
        given_names=given_names,
        family_names=family_names,
        delivery_place=delivery_place,
        phone_number=phone_number,
        country_phone_code=country_phone_code
    ))
    return {}


@router.delete('/{client_id}', dependencies=[Depends(bearer_scheme), Depends(jwt_guard)])
async def delete_client(client_id: str, command_bus: CommandBus = Depends(get_command_bus)):
    """Delete a client by its ID."""
    await command_bus.dispatch(DeleteClientCommand.create(client_id))
    return {}
