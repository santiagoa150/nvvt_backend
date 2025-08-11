from typing import Optional

from receipts.application.command.create_client_receipt.create_client_receipt_command import CreateClientReceiptCommand
from receipts.application.command.create_client_receipt.create_client_receipt_command_handler import \
    CreateClientReceiptCommandHandler
from receipts.infrastructure.reportlab.reportlab_receipt_generator import ReportlabReceiptGenerator
from shared import get_query_bus
from shared.domain.cqrs.command.command_handler import command_handler

_reportlab_receipt_generator: Optional[ReportlabReceiptGenerator] = None


async def get_reportlab_receipt_generator() -> ReportlabReceiptGenerator:
    """Returns an instance of ReportlabReceiptGenerator."""

    global _reportlab_receipt_generator

    if _reportlab_receipt_generator is None:
        _reportlab_receipt_generator = ReportlabReceiptGenerator()

    return _reportlab_receipt_generator


@command_handler(CreateClientReceiptCommand)
async def create_client_receipt_command_handler() -> CreateClientReceiptCommandHandler:
    """Handles the creation of a client receipt."""
    query_bus = await get_query_bus()
    receipt_generator = await get_reportlab_receipt_generator()
    return CreateClientReceiptCommandHandler(query_bus, receipt_generator)
