import asyncio
import json
from typing import List

from fastapi import APIRouter, Body, Depends, Query, Request
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPBearer

from notifications.application.command import (
    MarkNotificationsAsSeenCommand,
    SendNotificationCommand,
)
from notifications.application.query import GetPaginatedNotificationsQuery
from notifications.infrastructure.broker.in_memory_notification_broker import (
    InMemoryNotificationBroker,
)
from notifications.notification_dependencies import get_notification_broker
from settings import settings
from shared import get_command_bus, get_query_bus
from shared.domain.cqrs.command.command_bus import CommandBus
from shared.domain.cqrs.query.query_bus import QueryBus
from shared.domain.pagination_dict import PaginationDict
from shared.infrastructure.jwt.jwt_guard import jwt_guard

router = APIRouter()
bearer_scheme = HTTPBearer()


@router.get("/", dependencies=[Depends(bearer_scheme), Depends(jwt_guard)])
async def get_paginated_notifications(
    request: Request,
    page: int = Query(1, description="Page number to retrieve"),
    limit: int = Query(20, description="Number of items per page"),
    query_bus: QueryBus = Depends(get_query_bus),
):
    """Retrieve the authenticated user's paginated notifications, unseen ones first."""
    pagination = await query_bus.query(
        GetPaginatedNotificationsQuery.create(
            recipient=request.state.user["user_id"], page=page, limit=limit
        )
    )
    return PaginationDict(
        data=[notification.to_dict() for notification in pagination["data"]],
        metadata=pagination["metadata"],
    )


@router.patch("/seen", dependencies=[Depends(bearer_scheme), Depends(jwt_guard)])
async def mark_notifications_as_seen(
    notification_ids: List[str] = Body(
        ..., embed=True, description="IDs of the notifications to mark as seen"
    ),
    command_bus: CommandBus = Depends(get_command_bus),
):
    """Mark the given notifications as seen."""
    await command_bus.dispatch(MarkNotificationsAsSeenCommand.create(notification_ids))
    return {}


@router.get("/stream", dependencies=[Depends(bearer_scheme), Depends(jwt_guard)])
async def stream_notifications(
    request: Request,
    broker: InMemoryNotificationBroker = Depends(get_notification_broker),
):
    """
    Streams notifications addressed to the authenticated user over
    Server-Sent Events, for as long as the connection stays open.

    Since there's no reverse proxy or load balancer configuration in this
    project to guarantee idle SSE connections are kept open indefinitely, a
    heartbeat comment is sent on every quiet period to prevent intermediaries
    (proxies, gateways, browsers) from timing out the connection.
    """

    recipient = request.state.user["user_id"]
    queue = broker.subscribe(recipient)

    async def event_stream():
        try:
            while True:
                if await request.is_disconnected():
                    break

                try:
                    notification = await asyncio.wait_for(
                        queue.get(), timeout=settings.notification_heartbeat_interval_seconds
                    )
                    yield f"event: notification\ndata: {json.dumps(notification.to_dict())}\n\n"
                except asyncio.TimeoutError:
                    yield ": heartbeat\n\n"
        finally:
            broker.unsubscribe(recipient, queue)

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/test", dependencies=[Depends(bearer_scheme), Depends(jwt_guard)])
async def send_test_notification(
    request: Request,
    action: str = Body(..., description="Action of the test notification"),
    recipient: str = Body(
        None, description="Recipient user ID; defaults to the caller's own user ID"
    ),
    command_bus: CommandBus = Depends(get_command_bus),
):
    """
    Test-support endpoint: sends a notification through the same path a real
    one would take, so a client's SSE connection can be exercised manually.
    """
    await command_bus.dispatch(
        SendNotificationCommand.create(
            action=action,
            recipient=recipient or request.state.user["user_id"],
        )
    )
    return {}
