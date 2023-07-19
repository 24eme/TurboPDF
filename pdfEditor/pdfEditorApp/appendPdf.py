from PyPDF2 import PdfMerger
import os


def append_pdf_file(file_list):
    merger = PdfMerger()

    for file_path in file_list:
        with open(file_path, 'rb') as pdf:
            merger.append(pdf)

    with open("output_file.pdf", 'wb') as output:
        merger.write(output)

    print("function done in ", os.getcwd())
