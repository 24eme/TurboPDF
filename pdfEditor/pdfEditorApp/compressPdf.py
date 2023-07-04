from PyPDF2 import PdfReader, PdfWriter
import os

def compressPdfFunction(file):

    reader = PdfReader(file)
    writer = PdfWriter()

    for page in reader.pages:
        page.compress_content_streams()  # This is CPU intensive!
        writer.add_page(page)

    with open("compressedPDF.pdf", "wb") as f:
        writer.write(f)
    return os.path.getsize("compressedPDF.pdf")