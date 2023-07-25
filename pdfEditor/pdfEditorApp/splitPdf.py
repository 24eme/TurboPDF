from PyPDF2 import PdfReader, PdfWriter
import os
import re

def is_valid_page(page, max_page):
    try:
        page_number = int(page)
        return 1 <= page_number <= max_page
    except ValueError:
        return False

def split_keep_sep(text):
    pattern = r"([?]|[?]?[0-9]+|[^a-zA-Z0-9?]+)"
    return [elem for elem in re.split(pattern, text) if elem != '']

def split_pdf_pages(uploaded_file, element):
    if not element.strip():
        raise ValueError("L'élément pour l'extraction des pages est vide.")

    pdf_reader = PdfReader(uploaded_file)
    max_page = len(pdf_reader.pages)

    solo_page = 0

    start = 1
    end = max_page

    elements = split_keep_sep(element)
    if len(elements) == 3:
        start = int(elements[0]) if elements[0].isdigit() else start
        end = int(elements[2]) if elements[2].isdigit() else end
    elif len(elements) == 2:
        if elements[0] == '-' and elements[1].isdigit():
            end = int(elements[1])
            start = 0
        elif elements[0].isdigit() and elements[1] == '-':
            start = int(elements[0])
        else:
            raise ValueError("L'élément pour l'extraction des pages est invalide.")
    elif len(elements) == 1:
        if elements[0].isdigit():
            start = int(elements[0])
            solo_page = 1
        elif elements[0] == '-':
            start = 1
            end = max_page

    start = max(1, start)
    end = min(max_page, end)
    if not (1 <= start < max_page and 1 < end <= max_page and start < end):
        print(f"Attention : l'élément '{element}' contient des pages invalides et sera ignoré.")
        return None

    pdf_writer = PdfWriter()
    if solo_page == 0:
        for page_number in range(start - 1, end):
            pdf_writer.add_page(pdf_reader.pages[page_number])
    else:
        pdf_writer.add_page(pdf_reader.pages[start - 1])

    temp_output_file = f'extracted_pages_{element}.pdf'
    with open(temp_output_file, 'wb') as output:
        pdf_writer.write(output)

    with open(temp_output_file, 'rb') as file:
        file_data = file.read()

    os.remove(temp_output_file)

    return file_data
