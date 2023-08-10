import sys
import os
from PyPDF2 import PdfReader, PdfWriter

def unlock_pdf_file(input_file, password):
    reader = PdfReader(input_file)
   
    if not reader.decrypt(password):
        return False

    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    file_path = "savedFile.pdf"
    with open(file_path, "wb") as f:
        writer.write(f)

    return True

def is_pdf_encrypted(input_file):
    try:
        reader = PdfReader(input_file)
        return reader.is_encrypted
    except Exception as e:
        print("Error while checking PDF encryption:", str(e))
        return False