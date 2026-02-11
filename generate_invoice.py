from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import CondPageBreak

from datetime import date, timedelta

import random

OUTPUT_FILE = "invoice_sample.pdf"


# ------------------------
# Header and Footer
# ------------------------

def header_footer(canvas, doc):
    canvas.saveState()

    canvas.setFont("Helvetica", 9)

    # Top header line
    canvas.drawString(25*mm, 285*mm, "Atlantic Services Lda")
    canvas.drawRightString(190*mm, 285*mm, "Invoice")

    # separator line
    canvas.line(25*mm, 280*mm, 190*mm, 280*mm)

    # footer
    canvas.setFont("Helvetica", 8)
    canvas.drawString(25*mm, 12*mm, "Atlantic Services Lda - billing@atlanticservices.pt")
    
    canvas.restoreState()


# ------------------------
# Page numbering
# ------------------------

class PageNumCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """Add page numbers to all pages."""
        page_count = len(self._saved_page_states)

        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(page_count)
            super().showPage()

        super().save()

    def draw_page_number(self, total_pages):
        page = self._pageNumber
        text = f"Page {page} of {total_pages}"
        self.setFont("Helvetica", 9)
        self.drawRightString(200 * mm, 15 * mm, text)


# ------------------------
# Sample dynamic data
# ------------------------

def get_items():
    """Generate many rows to force multipage."""
    items = []
    services = [
        "Monthly SaaS Subscription",
        "Cloud Storage Usage",
        "API Requests Package",
        "Data Processing",
        "Priority Support",
        "Analytics Processing",
        "System Integration",
        "Custom Automation",
        "Monitoring Service",
        "Backup Retention"
    ]

    for i in range(50):  # enough to force page break
        qty = random.randint(1, 5)
        price = random.randint(20, 120)
        items.append((random.choice(services), qty, price, qty * price))
    return items


# ------------------------
# Document building
# ------------------------

def build_invoice():
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        rightMargin=25*mm,
        leftMargin=25*mm,
        topMargin=15*mm,
        bottomMargin=20*mm
    )
    doc.title = "Invoice Sample"

    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    bold = styles["Heading3"]

    right = ParagraphStyle(
        name="right",
        parent=normal,
        alignment=TA_RIGHT
    )
    rightBold = ParagraphStyle(
        name="right",
        parent=bold,
        alignment=TA_RIGHT
    )

    story = []

    # ------------------------
    # Logo - Company
    # ------------------------
    logo = Image("logo.png", width=60*mm, height=40*mm)
    story.insert(0, logo)
    story.insert(1, Spacer(1, 12))


    # ------------------------
    # Header - Company
    # ------------------------

    story.append(Paragraph("<b>Atlantic Services Lda</b>", bold))
    story.append(Paragraph("Rua Exemplo 123", normal))
    story.append(Paragraph("1200-001 Lisboa, Portugal", normal))
    story.append(Paragraph("Email: billing@atlanticservices.pt", normal))
    story.append(Paragraph("NIF: 509999999", normal))

    story.append(Spacer(1, 10))

    # ------------------------
    # Client block
    # ------------------------

    story.append(Paragraph("<b>Bill To:</b>", rightBold))
    story.append(Paragraph("TechSolutions GmbH", right))
    story.append(Paragraph("Alexanderplatz 3", right))
    story.append(Paragraph("10178 Berlin, Germany", right))
    story.append(Paragraph("VAT: DE123456789", right))

    story.append(Spacer(1, 25))

    # ------------------------
    # Invoice info
    # ------------------------

    invoice_number = f"INV-{date.today().year}-{random.randint(1000,9999)}"
    due_date = date.today() + timedelta(days=14)

    info_data = [
        ["Invoice Number:", invoice_number],
        ["Invoice Date:", str(date.today())],
        ["Due Date:", str(due_date)],
    ]

    info_table = Table(info_data, colWidths=[120, 200])
    info_table.setStyle(TableStyle([
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))

    story.append(info_table)
    story.append(Spacer(1, 20))

    # ------------------------
    # Items table
    # ------------------------

    items = get_items()

    table_data = [["Description", "Qty", "Unit Price (€)", "Total (€)"]]

    subtotal = 0
    for desc, qty, price, total in items:
        table_data.append([
            Paragraph(desc, normal), 
            qty, 
            f"{price:.2f}", 
            f"{total:.2f}"]
        )
        subtotal += total

    items_table = Table(
        table_data,
        repeatRows=1,
        colWidths=[90*mm, 20*mm, 30*mm, 30*mm]
    )


    items_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EAEAEA")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
    ]))

    story.append(items_table)
    story.append(Spacer(1, 20))

    # ------------------------
    # Totals
    # ------------------------

    vat = subtotal * 0.23
    total = subtotal + vat

    totals_data = [
        ["Subtotal:", f"{subtotal:.2f} €"],
        ["VAT (23%):", f"{vat:.2f} €"],
        ["Total:", f"{total:.2f} €"],
    ]

    totals_table = Table(totals_data, colWidths=[350, 100])
    totals_table.setStyle(TableStyle([
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
    ]))

    story.append(totals_table)
    story.append(Spacer(1, 24))

    story.append(CondPageBreak(80*mm))  # Force page break to show multipage handling

    # ------------------------
    # Payment info
    # ------------------------

    story.append(Paragraph("<b>Payment Details</b>", bold))
    story.append(Paragraph("IBAN: PT50 0000 0000 0000 0000 0000 0", normal))
    story.append(Paragraph("BIC/SWIFT: BCOMPTPL", normal))

    story.append(Spacer(1, 24))

    # ------------------------
    # Footer text
    # ------------------------

    story.append(Paragraph(
        "This invoice was generated electronically and is valid without signature.",
        right
    ))

    # Build
    doc.build(story, 
        onFirstPage=header_footer,
        onLaterPages=header_footer,
        canvasmaker=PageNumCanvas
    )


if __name__ == "__main__":
    build_invoice()
    print("Invoice generated:", OUTPUT_FILE)
