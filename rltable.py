from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib import colors

# Create a PDF
pdf = SimpleDocTemplate("table_example.pdf", pagesize=A4)

# Table data
data_p1 = [
    ['Jrk', '1. päev/1. väljak', 'KOHTUNIKUD', 'AEG'],
  [1, 'Pärnu spordikool II (R.E.) - Narva SK Energia/SK Galla I', '', '15:00'],
  [1, 'Jõhvi spordikool - Kuues võistkond', '', '16:15'],
  [1, 'Jõhvi spordikool - Pärnu spordikool II (R.E.)', '', '17:30'],
  [1,
   'Narva SK Energia/SK Galla II - Narva SK Energia/SK Galla I',
   '',
   '18:45']
]

data_p2 = [
['Jrk', '1. päev/2. väljak', 'KOHTUNIKUD', 'AEG'],
  [1, 'Paide Võrkpalliklubi - Narva SK Energia/SK Galla II', '', '15:00'],
  [1, 'Narva SK Energia/SK Galla I - Paide Võrkpalliklubi', '', '16:15'],
  [1, 'Kuues võistkond - Narva SK Energia/SK Galla II', '', '17:30'],
  [1, 'Pärnu spordikool II (R.E.) - Paide Võrkpalliklubi', '', '18:45']
]

data_p3 = [
['Jrk', '2. päev/1. väljak', 'KOHTUNIKUD', 'AEG'],
  [1, 'Pärnu spordikool II (R.E.) - Kuues võistkond', '', '11:00'],
  [1, 'Paide Võrkpalliklubi - Jõhvi spordikool', '', '12:15'],
  [1, 'Narva SK Energia/SK Galla II - Pärnu spordikool II (R.E.)', '', '13:30'],
  [1, 'Narva SK Energia/SK Galla I - Jõhvi spordikool', '', '14:45']
]

data_p4 = [
 ['Jrk', '2. päev/2. väljak', 'KOHTUNIKUD', 'AEG'],
  [1, 'Jõhvi spordikool - Narva SK Energia/SK Galla II', '', '11:00'],
  [1, 'Kuues võistkond - Narva SK Energia/SK Galla I', '', '12:15'],
  [1, 'Paide Võrkpalliklubi - Kuues võistkond', '', '13:30'],
  [1, ' - ', '', '14:45']
]


# Create table object
table_p1 = Table(data_p1)
table_p2 = Table(data_p2)
table_p3 = Table(data_p3)
table_p4 = Table(data_p4)

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

table_p3.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ("FONT", (0, 0), (-1, -1), "Helvetica"),
]))

table_p4.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ("FONT", (0, 0), (-1, -1), "Helvetica"),
]))


# Build PDF
pdf.build([table_p1, Spacer(0, 20), table_p2, Spacer(0, 20), table_p3, Spacer(0, 20), table_p4])


