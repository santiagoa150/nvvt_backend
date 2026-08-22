from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from countries.application.query import GetAllCountriesQuery
from countries.domain.country import Country
from shared import get_query_bus
from shared.domain.cqrs.query.query_bus import QueryBus
from shared.infrastructure.jwt.jwt_guard import jwt_guard

router = APIRouter()
bearer_scheme = HTTPBearer()


@router.get("/", dependencies=[Depends(bearer_scheme), Depends(jwt_guard)])
async def get_all_countries(query_bus: QueryBus = Depends(get_query_bus)):
    """Retrieve all countries."""
    countries: List[Country] = await query_bus.query(GetAllCountriesQuery.create())
    return [country.to_dict() for country in countries]
