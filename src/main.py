import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from shared import get_query_bus, get_command_bus, get_mongo_client
from shared.domain.exceptions.common_exception import CommonException
from campaigns.infrastructure.http import http_campaign_router
from shared.domain.exceptions.common_exception_messages import CommonExceptionMessages

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s (%(asctime)s): %(name)s - %(funcName)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(_):
    """Lifespan context manager for the FastAPI application."""

    # Initialize CQRS components
    await get_query_bus()
    await get_command_bus()

    # Initialize MongoDB connection
    client = get_mongo_client()

    yield
    # Cleanup actions can be added here if needed
    client.client.close()


def init_exception_handlers(api: FastAPI):
    """Initializes the exception handlers for the FastAPI application."""

    @api.exception_handler(CommonException)
    async def service_exception_handler(_, error: CommonException):
        return JSONResponse(error.to_dict(), status_code=error.code)

    @api.exception_handler(Exception)
    async def server_exception_handler(_, error: Exception):
        logger.error('Unhandled exception occurred', exc_info=error)
        return JSONResponse({
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': CommonExceptionMessages.INTERNAL_SERVER_ERROR.value,
        })


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


app = FastAPI(lifespan=lifespan)

init_exception_handlers(app)
init_routes(app)
