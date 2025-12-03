from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib import colors


def loo_pdf(võistlustabelid):
    # Create a PDF
    pdf = SimpleDocTemplate("table_example.pdf", pagesize=A4)

    pdftabelid = []
    for i, vtabel in enumerate(võistlustabelid):
        pdftabel = Table(vtabel)
        pdftabel.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("FONT", (0, 0), (-1, -1), "Helvetica"),
        ]))
        pdftabelid.append(pdftabel)
        if i != len(võistlustabelid) - 1:
            pdftabelid.append(Spacer(0, 20))

    for t in pdftabelid:
        pdf.build(pdftabelid)


