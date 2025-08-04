from fastapi import APIRouter, Depends, Query, Body

from clients.application.command.create_client.create_client_command import CreateClientCommand
from clients.application.command.delete_client.delete_client_command import DeleteClientCommand
from clients.application.query.get_client_by_id.get_client_by_id_query import GetClientByIdQuery
from clients.application.query.get_paginated_clients.get_paginated_clients_query import GetPaginatedClientsQuery
from clients.domain.client import Client
from shared import get_query_bus, get_command_bus
from shared.domain.cqrs.command.command_bus import CommandBus
from shared.domain.cqrs.query.query_bus import QueryBus
from shared.domain.pagination_dict import PaginationDict
from shared.domain.value_objects.common.country_phone_code import CountryPhoneCode
from shared.domain.value_objects.common.phone_number import PhoneNumber
from shared.domain.value_objects.id_value_object import IdValueObject
from shared.domain.value_objects.pagination.limit_param import LimitParam
from shared.domain.value_objects.pagination.page_param import PageParam
from shared.domain.value_objects.string_value_object import StringValueObject

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


@router.post('/')
async def create_client(
        given_names: str = Body(..., description='Given names of the client'),
        family_names: str = Body(None, description='Family names of the client'),
        delivery_place: str = Body(..., description='Delivery place of the client'),
        phone_number: str = Body(None, description='Phone number of the client'),
        country_phone_code: int = Body(None, description='Country phone code of the client'),
        command_bus: CommandBus = Depends(get_command_bus)
):
    """Create a new client."""
    await command_bus.dispatch(CreateClientCommand(
        StringValueObject(given_names, 'client_given_names'),
        StringValueObject(family_names, 'client_family_names') if family_names else None,
        StringValueObject(delivery_place, 'client_delivery_place'),
        PhoneNumber(phone_number, 'client_phone_number') if phone_number else None,
        CountryPhoneCode(country_phone_code, 'client_country_phone_code') if country_phone_code else None,
    ))
    return {}


@router.get('/{client_id}')
async def get_client_by_id(client_id: str, query_bus: QueryBus = Depends(get_query_bus)):
    """Retrieve a client by its ID."""
    client: Client = await query_bus.query(GetClientByIdQuery(
        IdValueObject(client_id, 'client_id')
    ))
    return client.to_dict()


@router.delete('/{client_id}')
async def delete_client(client_id: str, command_bus: CommandBus = Depends(get_command_bus)):
    """Delete a client by its ID."""
    await command_bus.dispatch(DeleteClientCommand(
        IdValueObject(client_id, 'client_id')
    ))
    return {}
