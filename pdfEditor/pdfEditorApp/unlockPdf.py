import sys
import os
from PyPDF2 import PdfReader, PdfWriter

def unlock_pdf_file(input_file, password):
    reader = PdfReader(input_file)

    if reader.is_encrypted:
        if not reader.decrypt(password):
            print("Wrong password.")
            exit()

    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    file_path = "savedFile.pdf"
    with open(file_path, "wb") as f:
        writer.write(f)
