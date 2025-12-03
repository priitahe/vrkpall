# import the canvas object
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4

# create a Canvas object with a filename
c = canvas.Canvas("rl-hello_again.pdf", pagesize=A4)  # A4 pagesize
# draw a string at x=100, y=800 points
# point ~ standard desktop publishing (72 DPI)
# coordinate system:
#   y
#   |
#   |   page
#   |
#   |
#   0-------x
c.drawString(50, 780, "Tere, Maailm!")
# finish page
c.showPage()
# construct and save file to .pdf
c.save()