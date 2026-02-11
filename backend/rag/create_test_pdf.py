from fpdf import FPDF
import os

PDF_FOLDER = "../django/syllabus"
os.makedirs(PDF_FOLDER, exist_ok=True)  # ensure folder exists

pdf_path = os.path.join(PDF_FOLDER, "test.pdf")

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, "This is a test PDF for the GCE AI Tutor project.\nIt contains some sample content for ingestion.\nIdeal gas law: PV = nRT.\nWater boils at 100 degrees Celsius.\nMath example: 2 + 2 = 4")
pdf.output(pdf_path)

print(f"✅ Test PDF created at {pdf_path}")
