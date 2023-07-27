import os
import zipfile
import shutil
from PyPDF2 import PdfReader
from PIL import Image
from pdf2image import convert_from_path

def pdf_to_png(input_pdf_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    images = convert_from_path(input_pdf_path)

    for page_num, image in enumerate(images):
        output_path = os.path.join(output_folder, f'page_{page_num + 1}.png')
        image.save(output_path, 'PNG')


def extract_images_from_pdf(pdf_file, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    with open(pdf_file, "rb") as file:
        pdf_reader = PdfReader(file)
        num_pages = len(pdf_reader.pages)

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            if '/Resources' in page:
                resources = page['/Resources'].get_object()
                if '/XObject' in resources:
                    xObject = resources['/XObject'].get_object()

                    for obj in xObject:
                        if xObject[obj]['/Subtype'] == '/Image':
                            size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                            data = xObject[obj].get_object()

                            if '/Filter' in data:
                                if data['/Filter'] == '/FlateDecode':
                                    img = Image.frombytes('RGB', size, data.get_data())
                                    img.save(f"{output_folder}/image_page_{page_num + 1}.png")
                                elif data['/Filter'] == '/DCTDecode':
                                    with open(f"{output_folder}/image_page_{page_num + 1}.jpg", "wb") as img_file:
                                        img_file.write(data.get_data())
                                elif data['/Filter'] == '/JPXDecode':
                                    with open(f"{output_folder}/image_page_{page_num + 1}.jp2", "wb") as img_file:
                                        img_file.write(data.get_data())

    print("Image extraction completed.")

def zip_folder(input_folder, output_zip):
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(input_folder):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, arcname=os.path.relpath(file_path, start=input_folder))
    #supprimer le dossier
    try:
        shutil.rmtree(input_folder)
    except Exception as e:
        print(f"Erreur lors de la suppression du répertoire : {e}")

