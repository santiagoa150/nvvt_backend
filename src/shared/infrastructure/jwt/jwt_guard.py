from fastapi import Depends, Request

from auth.application.query.verify_user_access_token.verify_user_access_token_query import (
    VerifyUserAccessTokenQuery,
)
from auth.domain.auth_data import AuthData
from auth.domain.exceptions.unauthorized_exception import UnauthorizedException
from shared import get_query_bus
from shared.domain.cqrs.query.query_bus import QueryBus


async def jwt_guard(request: Request, query_bus: QueryBus = Depends(get_query_bus)):
    """
    JWT authentication guard to protect routes.

    :param request: FastAPI request object.
    :param query_bus: QueryBus instance for handling queries.
    :return:
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise UnauthorizedException.user_not_authenticated()

    token = auth_header.split(" ")[1]
    payload: AuthData = await query_bus.query(VerifyUserAccessTokenQuery(access_token=token))
    if payload is None:
        raise UnauthorizedException.user_not_authenticated()

    request.state.user = payload
