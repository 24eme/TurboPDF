from PyPDF2 import PdfReader, PdfWriter
from django.shortcuts import render
from django.http import HttpResponse, FileResponse, Http404
from django.shortcuts import render
from pdfEditorApp.listing.forms import inputForm
from pdfEditorApp.compressPdf import compressPdfFunction
from pdfEditorApp.lockPdf import lock_pdf_file, save_input_file
import os


# Create your views here.
def addImage(request):

    return render(request, 'addImage.html')
def compressPdf(request):
    compressedFileSize = None
    form = inputForm()
    if request.method == 'POST':
        compressedFileSize = compressPdfFunction(request.FILES['pdf_file'])
        print('your file was compressed ', compressedFileSize)
    else:
        form = inputForm()
    return render(request, 'compressPdf.html', {'compressedFileSize': compressedFileSize})

def download_compressed(request):
    if os.path.exists("compressedPDF.pdf"):
        with open("compressedPDF.pdf", 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="compressed.pdf"'
            response['Content-Length'] = os.path.getsize("compressedPDF.pdf")
            response['Content-Disposition'] += 'attachment; filename*=UTF-8\'\'compressed.pdf'
            return response
    else:
        return HttpResponse("The compressed file does not exist.")

def lockPdf(request):
    form = inputForm() #enlever cela ppour voir si ca va marcher
    print(form)
    if request.method == 'POST':
        password = request.POST['password']
        input_path = save_input_file(request.FILES['input_file'])
        lock_pdf_file(input_path, password)
    
    return render(request, 'lockPdf.html')

def download_locked_file(request):
    if os.path.exists("encrypted_lockedFile.pdf"):
        with open("encrypted_lockedFile.pdf", 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="encrypted_lockedFile.pdf"'
            response['Content-Length'] = os.path.getsize("encrypted_lockedFile.pdf")
            response['Content-Disposition'] += 'attachment; filename*=UTF-8\'\'encrypted_lockedFile.pdf'
            return response
    else:
        return HttpResponse("Error while downloading the file")


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


