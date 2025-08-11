from io import BytesIO
from typing import List

from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm

from campaigns.domain.campaign import Campaign
from clients.domain.client import Client
from orders.domain.order import Order
from receipts.domain.repository.receipt_generator import ReceiptGenerator


class ReportlabReceiptGenerator(ReceiptGenerator):
    """Generates receipts using the ReportLab library."""

    def __init__(self):
        """Initialize the ReportlabReceiptGenerator."""
        self._styles = getSampleStyleSheet()
        self._custom_colors = {
            'primary': colors.HexColor("#1f96ab"),
            'text': colors.HexColor("#4a4a4a"),
        }
        self._custom_styles = {
            'texts': {
                'normal': ParagraphStyle(
                    name='BaseText',
                    parent=self._styles['Normal'],
                    fontName='Helvetica',
                    textColor=self._custom_colors['text'],
                ),
                'white': ParagraphStyle(
                    name='WhiteText',
                    parent=self._styles['Normal'],
                    fontName='Helvetica',
                    textColor=colors.white
                ),
                'title': ParagraphStyle(
                    name='CustomTitle',
                    parent=self._styles['Title'],
                    fontName='Helvetica',
                    alignment=0,
                    textColor=self._custom_colors['text'],
                ),
                'small': ParagraphStyle(
                    name='SmallText',
                    parent=self._styles['Normal'],
                    fontName='Helvetica',
                    fontSize=8,
                    textColor=self._custom_colors['text'],
                )
            }
        }

    async def create_client_receipt(self, campaign: Campaign, client: Client, orders: List[Order]) -> BytesIO:
        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer, pagesize=A4)
        available_width = A4[0] - doc.leftMargin - doc.rightMargin

        # Title configuration
        title = Paragraph(
            f"Detalle de tu pedido <b>Campaña {campaign.year.int} - {campaign.number.int}</b>",
            self._custom_styles['texts']['title']
        )

        # Client Configuration
        cliente_data = [
            [Paragraph("<b>Cliente</b>", self._custom_styles['texts']['normal']),
             Paragraph(client.full_name.str, self._custom_styles['texts']['normal'])],
            [Paragraph('<b>Dirección</b>', self._custom_styles['texts']['normal']),
             Paragraph(client.delivery_place.str, self._custom_styles['texts']['normal'])]
        ]

        if client.phone:
            cliente_data.append([
                Paragraph("<b>Teléfono</b>", self._custom_styles['texts']['normal']),
                Paragraph(client.phone.to_e164(), self._custom_styles['texts']['normal'])
            ])

        cliente_table = Table(cliente_data, colWidths=[0.15 * available_width, 0.85 * available_width])
        cliente_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "LEFT"),
            ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#007C91")),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))

        # Summary Configuration
        total_products = sum(order.quantity.int for order in orders)
        total_catalog_price = sum(order.product.catalog_price.float * order.quantity.int for order in orders)

        summary = [
            [
                Paragraph("<b>TOTAL PRODUCTOS</b>", self._custom_styles['texts']['white']),
                Paragraph("<b>PRECIO</b>", self._custom_styles['texts']['white']),
            ],
            [
                Paragraph(f"{total_products}", self._custom_styles['texts']['normal']),
                Paragraph(f"${total_catalog_price:,.0f}", self._custom_styles['texts']['normal']),
            ]
        ]

        summary_table = Table(summary, colWidths=[available_width / 2] * 2)
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self._custom_colors['primary']),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f8f8f8")),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        # Products Configuration
        products_title_table = Table(
            [[Paragraph("<b>TUS PRODUCTOS</b>", self._custom_styles['texts']['white'])]],
            colWidths=[available_width]
        )
        products_title_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self._custom_colors['primary']),
        ]))
        products = [
            [
                Paragraph("<b>Código</b>", self._custom_styles['texts']['small']),
                Paragraph("<b>Descripción</b>", self._custom_styles['texts']['small']),
                Paragraph("<b>Cant.</b>", self._custom_styles['texts']['small']),
                Paragraph("<b>Valor Unidad</b>", self._custom_styles['texts']['small']),
                Paragraph("<b>Total</b>", self._custom_styles['texts']['small']),
            ]
        ]
        products = products + [
            [
                Paragraph(order.product.code.str, self._custom_styles['texts']['small']),
                Paragraph(order.product.name.str, self._custom_styles['texts']['small']),
                Paragraph(str(order.quantity.int), self._custom_styles['texts']['small']),
                Paragraph(f"${order.product.catalog_price.float:,.0f}",
                          self._custom_styles['texts']['small']),
                Paragraph(f"${(order.product.catalog_price.float * order.quantity.int):,.0f}",
                          self._custom_styles['texts']['small'])
            ] for order in orders
        ]
        products_table = Table(products, colWidths=[
            0.12 * available_width,
            0.52 * available_width,
            0.08 * available_width,
            0.14 * available_width,
            0.14 * available_width,
        ])
        products_table.setStyle(TableStyle([
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.lightgrey]),
            ("ALIGN", (0, 0), (0, -1), "CENTER"),
            ("ALIGN", (2, 0), (-1, -1), "CENTER"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))

        doc.build([
            title,
            HRFlowable(width="100%", thickness=1, color=colors.black),
            Spacer(1, 0.5 * cm),
            cliente_table,
            Spacer(1, 0.5 * cm),
            summary_table,
            Spacer(1, 0.5 * cm),
            products_title_table,
            products_table,
        ])
        buffer.seek(0)

        return buffer
