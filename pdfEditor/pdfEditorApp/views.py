from PyPDF2 import PdfReader, PdfWriter
from django.http import HttpResponse, FileResponse, Http404, JsonResponse
from django.shortcuts import render
from pdfEditorApp.listing.forms import inputForm
from pdfEditorApp.lockPdf import lock_pdf_file, save_input_file
from pdfEditorApp.unlockPdf import unlock_pdf_file
from pdfEditorApp.appendPdf import append_pdf_file
from pdfEditorApp.deletePagePdf import removePageFromPdf
from pdfEditorApp.compressPdf import compress
from pdfEditorApp.splitPdf import split_pdf_pages
from pdfEditorApp.pdfToImage import pdf_to_png, zip_folder, extract_images_from_pdf
import os, uuid, zipfile


# Create your views here.

def homePagePdf(request):
    return render(request, 'homePagePdf.html')

def addImage(request):
    return render(request, 'addImage.html')

def deletePagePdf(request):
    return render(request, 'deletePagePdf.html')
    
def fillFormPdf(request):
    return render(request, 'fillFormPdf.html')

def pdfToImage(request):
    output_folder = 'output_images'
    output_zip = 'output_images.zip'
    if request.method == 'POST':
        input_path = save_input_file(request.FILES['input_file'])

        # Vérifier quel bouton a été cliqué
        if 'filename' in request.POST:
            pdf_to_png(input_path,output_folder)
        else:
            print("extract images")
            extract_images_from_pdf(input_path, output_folder)
            
        zip_folder(output_folder,output_zip)
        #download the zipped folder
        with open(output_zip, 'rb') as zip_file:
            response = HttpResponse(zip_file.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{output_zip}"'
            response['Content-Length'] = os.path.getsize(output_zip)

        os.remove(output_zip)

        return response
    return render(request, 'pdfToImage.html')

def compressPdf(request):
    form = inputForm()
    compression_option = ''
    compression_value = ''
    final_size = 0
    initial_size = 0
    ratio = 0
    pdf_file = request.FILES.get('pdf_file')
    if request.method == 'POST':
        if pdf_file is not None:
            compression_option = request.POST.get('compressionValue')
            if compression_option == 'moyenne':
                (final_size, ratio, initial_size) = compress(pdf_file, 'CompressedPdf.pdf', power=3)

            elif compression_option == 'haute':
                (final_size, ratio, initial_size) = compress(pdf_file, 'CompressedPdf.pdf', power=4)

    final_ratio = int(ratio)
    final_size = round(final_size, 3)
    initial_size = round(initial_size, 3)
    return render(request, 'compressPdf.html', {'final_size': round(final_size / 1024, 1), 'final_ratio': final_ratio, 'initial_size': round(initial_size / 1024, 1),'compression_option':compression_option})



def appendPdf(request):
    if request.method == 'POST':
        merged_file_path = 'grouped_file.pdf'
        uploaded_files = []

        files = request.FILES.getlist('pdf-upload[]')
        for file in files:
            unique_filename = f"{str(uuid.uuid4())}.pdf"  # Generate a unique filename for each file
            with open(unique_filename, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            uploaded_files.append((unique_filename, file.name))  # Store the tuple (unique_filename, original_filename)

        # Sort the uploaded_files list based on the order of appearance in the request.FILES list
        sorted_uploaded_files = [unique_filename for unique_filename, _ in uploaded_files]

        append_pdf_file(sorted_uploaded_files, merged_file_path)

        return download_append_file(merged_file_path, uploaded_files)

    return render(request, 'appendPdf.html')


def download_append_file(file_path, uploaded_files):
    if os.path.exists(file_path):
        # Get the original filenames in the order they were uploaded
        original_filenames = [original_filename for _, original_filename in uploaded_files]

        # Merge the files in the order of their original filenames
        sorted_uploaded_files = [filename for filename in original_filenames]

        append_pdf_file(sorted_uploaded_files, file_path)

        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            response['Content-Length'] = os.path.getsize(file_path)
            response['Content-Disposition'] += f'attachment; filename*=UTF-8\'\'{os.path.basename(file_path)}'

        # Delete the merged file after download
        os.remove(file_path)

        # Delete the uploaded files
        for uploaded_file in uploaded_files:
            os.remove(uploaded_file)

        return response
    else:
        return HttpResponse("Error while downloading the file")



def lockPdf(request):
    if request.method == 'POST':
        password = request.POST['password']
        input_path = save_input_file(request.FILES['input_file'])
        lock_pdf_file(input_path, password)
        # Renvoyer le fichier verrouillé en téléchargement
        encrypted_file_path = "encrypted_File.pdf"
        if os.path.exists(encrypted_file_path):
            with open(encrypted_file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="encrypted_File.pdf"'
                response['Content-Length'] = os.path.getsize(encrypted_file_path)
                response['Content-Disposition'] += 'attachment; filename*=UTF-8\'\'encrypted_File.pdf'
                os.remove(encrypted_file_path)  
                return response
        else:
            return HttpResponse("Error while locking and downloading the file")

    return render(request, 'lockPdf.html')



def unlockPdf(request):
    if request.method == 'POST':
        password = request.POST['password']
        unlock_pdf_file(request.FILES['input_file'], password)

        decrypted_file_path = "savedFile.pdf"
        if os.path.exists(decrypted_file_path):
            with open("savedFile.pdf", 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="savedFile.pdf"'
                response['Content-Length'] = os.path.getsize(decrypted_file_path)
                response['Content-Disposition'] += 'attachment; filename*=UTF-8\'\'savedFile.pdf'
                os.remove(decrypted_file_path)
                return response
        else:
            return HttpResponse("Error while downloading the file")
            
    return render(request, 'unlockPdf.html')


def displayPdf(request):
    if request.method == 'POST':
        pdf_file = request.FILES['pdf_file']

        reader = PdfReader(pdf_file)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)
        myFile = "myFile.pdf"
        with open(myFile, "wb") as f:
            writer.write(f)
        if myFile:
            return FileResponse(open(myFile, 'rb'), content_type='application/pdf')
        else:
            return render(request, 'error_template.html', {'message': "The requested PDF file doesn't exist."})
    return render(request, 'displayPdf.html')

def download_compressed(request):
    if os.path.exists("CompressedPdf.pdf"):
        with open("CompressedPdf.pdf", 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="CompressedPdf.pdf"'
            response['Content-Length'] = os.path.getsize("CompressedPdf.pdf")
            response['Content-Disposition'] += 'attachment; filename*=UTF-8\'\'CompressedPdf.pdf'

            os.remove('CompressedPdf.pdf')
            return response
    else:
        return HttpResponse("Error while downloading the file")

def splitPdf(request):
    if request.method == 'POST':
        split_pdf_file = []
        tab_page_selection = request.POST.get('page_selection', '').split(',')
        uploaded_file = None
        for file_name, file in request.FILES.items():
            with open('uploaded_file.pdf', 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            uploaded_file = 'uploaded_file.pdf'

        for index, element in enumerate(tab_page_selection, 1):
            if element == "":
                continue;
            file_data = split_pdf_pages(uploaded_file, element)
            if file_data is not None:
                split_pdf_file.append((f'file_{index}.pdf', file_data))

        os.remove('uploaded_file.pdf')  # Remove the uploaded file

        # Vérifier le nombre de fichiers extraits
        if len(split_pdf_file) == 1:
            filename, file_data = split_pdf_file[0]
            response = HttpResponse(file_data, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            response['Content-Length'] = len(file_data)
            return response
        else:
            # S'il y a plusieurs fichiers, créer un fichier ZIP et les compresser dedans
            zip_filename = 'extracted_files.zip'
            with zipfile.ZipFile(zip_filename, 'w') as zip_file:
                for filename, file_data in split_pdf_file:
                    zip_file.writestr(filename, file_data)

            with open(zip_filename, 'rb') as zip_file:
                response = HttpResponse(zip_file.read(), content_type='application/zip')
                response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
                response['Content-Length'] = os.path.getsize(zip_filename)

            os.remove(zip_filename)

            return response

    return render(request, 'splitPdf.html')

def modifyText(request):
  
    return render(request, 'modifyText.html')

