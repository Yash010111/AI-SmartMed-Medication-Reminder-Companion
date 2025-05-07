from reportlab.pdfgen import canvas
from io import BytesIO

def create_pdf():
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    
    # Add prescription content
    p.drawString(100, 750, "Prescription Details:")
    p.drawString(100, 730, "Patient Name: John Doe")
    p.drawString(100, 710, "Date: 2023-10-15")
    p.drawString(100, 690, "Doctor: Dr. Smith")
    p.drawString(100, 670, "Medications:")
    p.drawString(120, 650, "1. Paracetamol 500mg - 1 tablet at 15:15")
    p.drawString(120, 630, "2. Amoxicillin 500mg - 1 capsule at 15:10")
    p.drawString(120, 610, "3. Cetirizine 10mg - 1 tablet at bedtime")
    # p.drawString(100, 590, "Instructions:")
    # p.drawString(120, 570, "- Take Paracetamol for fever and pain")
    # p.drawString(120, 550, "- Take Amoxicillin with food")
    # p.drawString(120, 530, "- Cetirizine may cause drowsiness")
    p.drawString(100, 510, "Follow up in 7 days.")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer.getvalue()

# Generate and save PDF
pdf_bytes = create_pdf()
with open("sample_prescription.pdf", "wb") as f:
    f.write(pdf_bytes)
