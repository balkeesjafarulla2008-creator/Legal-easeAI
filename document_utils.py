from docx import Document
from fpdf import FPDF
from io import BytesIO


def format_docx(text):
    doc = Document()

    for line in text.split("\n"):
        if line.strip():
            doc.add_paragraph(line)

    output = BytesIO()
    doc.save(output)
    output.seek(0)

    return output.getvalue()


def format_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=11)

    for line in text.split("\n"):
        pdf.multi_cell(0, 8, line)

    return bytes(pdf.output())