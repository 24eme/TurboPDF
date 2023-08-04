from PyPDF2 import PdfMerger


def append_pdf_file(input_files, output_file):
    merger = PdfMerger()


    for input_file in input_files:
        with open(input_file, 'rb') as pdf_file:
            merger.append(pdf_file)

    with open(output_file, 'wb') as output:
        merger.write(output)