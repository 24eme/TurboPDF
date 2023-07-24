from PyPDF2 import PdfReader, PdfWriter
from django.http import HttpResponse, FileResponse, Http404
from django.shortcuts import render
from pdfEditorApp.listing.forms import inputForm
from pdfEditorApp.lockPdf import lock_pdf_file, save_input_file
from pdfEditorApp.unlockPdf import unlock_pdf_file
from pdfEditorApp.appendPdf import append_pdf_file
from pdfEditorApp.deletePagePdf import removePageFromPdf
from pdfEditorApp.compressPdf import compress
import os


# Create your views here.

def homePagePdf(request):
    return render(request, 'homePagePdf.html')

def addImage(request):
    return render(request, 'addImage.html')

def deletePagePdf(request):
    return render(request, 'deletePagePdf.html')
    
def fillFormPdf(request):
    return render(request, 'fillFormPdf.html')

def compressPdf(request):
    form = inputForm()
    compression_option = ''
    compression_value = ''
    final_size = 0
    initial_size = 0
    ratio = 0
    pdf_file = request.FILES.get('pdf_file')
    if request.method == 'POST':
        compression_option = request.POST.get('compressionTypes')

        if compression_option == 'moyenne':
            (final_size, ratio, initial_size) = compress(pdf_file, 'CompressedPdf.pdf', power=3)
        elif compression_option == 'haute':
            (final_size, ratio, initial_size) = compress(pdf_file, 'CompressedPdf.pdf', power=4)

    final_ratio = int(ratio)
    final_size = round(final_size, 3)
    initial_size = round(initial_size, 3)
    return render(request, 'compressPdf.html', {'final_size': final_size, 'final_ratio': final_ratio, 'initial_size': initial_size,'compression_option':compression_option})


def appendPdf(request):
    download_status = 0
    if request.method == 'POST':
        download_status = 1
        uploaded_files = []
        for file_name, file in request.FILES.items():
            with open(file_name, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            uploaded_files.append(file_name)

        append_pdf_file(uploaded_files)
        os.remove('pdf-upload1')
        os.remove('pdf-upload2')

        return download_append_file(request)

    return render(request, 'appendPdf.html', {'download_status': download_status})

def download_append_file(request):
    if os.path.exists("grouped_file.pdf"):
        with open("grouped_file.pdf", 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="grouped_file.pdf"'
            response['Content-Length'] = os.path.getsize("grouped_file.pdf")
            response['Content-Disposition'] += 'attachment; filename*=UTF-8\'\'grouped_file.pdf'

            os.remove('grouped_file.pdf')
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
    return render(request, 'splitPdf.html')

def modifyText(request):
  
    return render(request, 'modifyText.html')

