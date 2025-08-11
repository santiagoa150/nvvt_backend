from fastapi import APIRouter, Depends, Response

from receipts.application.command.create_client_receipt.create_client_receipt_command import CreateClientReceiptCommand, \
    CreateClientReceiptCommandResponse
from shared import get_command_bus
from shared.domain.cqrs.command.command_bus import CommandBus

router = APIRouter()


@router.post('/by-client/{client_id}/by-campaign/{campaign_id}')
async def create_client_receipt(
        client_id: str,
        campaign_id: str,
        command_bus: CommandBus = Depends(get_command_bus)
):
    """Endpoint to create a receipt for a client by campaign."""
    result: CreateClientReceiptCommandResponse = await command_bus.dispatch(
        CreateClientReceiptCommand.create(campaign_id, client_id)
    )

    return Response(
        content=result['receipt'].getvalue(),
        media_type='application/pdf',
        headers={
            "Content-Disposition": f'attachment; filename="{result["title"]}"'
        }
    )
