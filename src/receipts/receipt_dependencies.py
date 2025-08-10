from typing import Optional

from receipts.infrastructure.reportlab.reportlab_receipt_generator import ReportlabReceiptGenerator

_reportlab_receipt_generator: Optional[ReportlabReceiptGenerator] = None


async def get_reportlab_receipt_generator() -> ReportlabReceiptGenerator:
    """Returns an instance of ReportlabReceiptGenerator."""

    global _reportlab_receipt_generator

    if _reportlab_receipt_generator is None:
        _reportlab_receipt_generator = ReportlabReceiptGenerator()

    return _reportlab_receipt_generator
