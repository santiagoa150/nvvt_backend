from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from settings import settings
from shared import get_query_bus, get_command_bus
from shared.domain.exceptions.common_exception import CommonException
from campaigns.infrastructure.http import http_campaign_router


def init_cqrs():
    """Initializes the CQRS components for the application."""

    get_query_bus()
    get_command_bus()


def init_exception_handlers(api: FastAPI):
    """Initializes the exception handlers for the FastAPI application."""

    @api.exception_handler(CommonException)
    async def service_exception_handler(_, error: CommonException):
        return JSONResponse(error.to_dict(), status_code=error.code)


def init_middlewares(api: FastAPI):
    """Initializes the middlewares for the FastAPI application."""

    api.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=False,
        allow_methods=['*'],
        allow_headers=['*'],
    )


def init_routes(api: FastAPI):
    """Initializes the routes for the FastAPI application."""

    api.include_router(http_campaign_router.router, prefix="/api/v1/campaigns", tags=["Campaigns"])


app = FastAPI()

init_cqrs()
init_exception_handlers(app)
init_routes(app)
