# from PyPDF2 import PdfReader, PdfWriter
from pypdf import PdfReader, PdfWriter
from PIL import Image
import os

def compressPdfFunction(file):

    reader = PdfReader(file) 
    writer = PdfWriter()

    for page in reader.pages: 
        writer.add_page(page)

    for page in writer.pages: 
        for img in page.images:
            img.replace(img.image, quality=60) 

    compFile = "compressedPDF.pdf"
    with open(compFile, "wb") as f:
        writer.write(f)
    return os.path.getsize("compressedPDF.pdf")


def highCompressionPdfFunction(file):
    reader = PdfReader(file) 
    writer = PdfWriter()

    for page in reader.pages: 
        writer.add_page(page)

    for page in writer.pages: 
        for img in page.images:
            img.replace(img.image, quality=3)
            
    highCompFile = "highCompressed.pdf"
    with open(highCompFile, "wb") as fp: 
        writer.write(fp)
    return os.path.getsize("highCompressed.pdf")

