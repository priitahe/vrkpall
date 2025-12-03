# import rml2pdf from rlextra
from rlextra.rml2pdf import rml2pdf

# open rml
with open("rlplus-hello_again.rml", "r") as rml:
    rml2pdf.go(rml.read(), "rlplus-hello_again.pdf")
    rml.close()