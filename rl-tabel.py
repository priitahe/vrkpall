from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib import colors

# Create a PDF
pdf = SimpleDocTemplate("table_example.pdf", pagesize=A4)

# Table data
data_p1 = [
    ['Jrk', '1. päev', 'KOHTUNIKUD', 'AEG'],
    ('a', 1, ''), ('b', 2, 'Trt'), ('c', 3, 'Nrv')
]

data_p2 = [
    ['Jrk', '2. päev', 'KOHTUNIKUD', 'AEG'],
    ('a', 1, ''), ('b', 2, 'Trt'), ('c', 3, 'Nrv')
]

# Create table object
table_p1 = Table(data_p1)
table_p2 = Table(data_p2)

# Style the table
table_p1.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ("FONT", (0, 0), (-1, -1), "Helvetica"),
]))

table_p2.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ("FONT", (0, 0), (-1, -1), "Helvetica"),
]))


# Build PDF
pdf.build([table_p1, Spacer(0, 20), table_p2])

