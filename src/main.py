from fastapi import FastAPI

from campaigns.infrastructure.http import http_campaign_router
from shared.shared_dependencies import get_query_bus, get_command_bus


def init_routes(api: FastAPI):
    """Initializes the routes for the FastAPI application."""

    api.include_router(http_campaign_router.router, prefix="/api/v1/campaigns", tags=["Campaigns"])


def init_cqrs():
    import campaigns # noqa: F401

    """Initializes the CQRS components for the application."""
    get_query_bus()
    get_command_bus()


app = FastAPI()

init_cqrs()
init_routes(app)
