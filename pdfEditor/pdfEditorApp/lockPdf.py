import sys
import os
import fitz
from django.conf import settings
from PyPDF2 import PdfReader, PdfWriter

def lock_pdf_file(input_file, password):
    doc = fitz.open(input_file)
    perm = int(fitz.PDF_PERM_ACCESSIBILITY)
    user_pass = password

    encrypt_meth = fitz.PDF_ENCRYPT_AES_256
    encrypted_file_name = "encrypted_" + os.path.basename(input_file)
    doc.save(encrypted_file_name, encryption=encrypt_meth, user_pw=user_pass, permissions=perm)
    
    #delete the input_file
    os.remove(input_file)


def save_input_file(input_file):
    reader = PdfReader(input_file)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)
    file_path = "File.pdf"
    with open(file_path, "wb") as f:
        writer.write(f)
    return file_path


