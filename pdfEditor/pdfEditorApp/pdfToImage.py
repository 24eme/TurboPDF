import os
import zipfile
import shutil
from pdf2image import convert_from_path

def pdf_to_png(input_pdf_path, output_folder):

    images = convert_from_path(input_pdf_path)

    for page_num, image in enumerate(images):
        output_path = os.path.join(output_folder, f'page_{page_num + 1}.png')
        image.save(output_path, 'PNG')

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)


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
        print(f"Erreur lors de la suppression du répertoire '{directory_path}': {e}")

