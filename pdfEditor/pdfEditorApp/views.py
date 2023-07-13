from PyPDF2 import PdfReader, PdfWriter
from django.shortcuts import render
from django.http import HttpResponse, FileResponse, Http404
from django.shortcuts import render
from pdfEditorApp.listing.forms import inputForm
from pdfEditorApp.lockPdf import lock_pdf_file, save_input_file
from pdfEditorApp.unlockPdf import unlock_pdf_file
from pdfEditorApp.deletePagePdf import removePageFromPdf
from pdfEditorApp.compressPdf import compress
import os


# Create your views here.
def homePagePdf(request):
    return render(request, 'homePagePdf.html')

def addImage(request):
    return render(request, 'addImage.html')

def deletepagePdf(request):
    return render(request, 'deletePage.html')

def compressPdf(request): 
    form = inputForm()
        
    if 'small-compression' in request.POST:
        compress(request.FILES['pdf_file'], 'smallCompressedPdf.pdf', power=2)
        print('your file was small compressed')

    elif 'medium-compression' in request.POST: 
        compress(request.FILES['pdf_file'], 'mediumCompressedPdf.pdf', power=3)
        print('your file was medium compressed')

    elif 'high-compression' in request.POST:
        compress(request.FILES['pdf_file'], 'highlyCompressedPdf.pdf', power=4)
        print('your file was highly compressed')

    return render(request, 'compressPdf.html')


def lockPdf(request):
    if request.method == 'POST':
        password = request.POST['password']
        input_path = save_input_file(request.FILES['input_file'])
        lock_pdf_file(input_path, password)
    return render(request, 'lockPdf.html')

def unlockPdf(request):
    if request.method == 'POST':
        password = request.POST['password']
        unlock_pdf_file(request.FILES['input_file'], password)
    return render(request, 'unlockPdf.html')

def download_locked_file(request):
    if os.path.exists("encrypted_File.pdf"):
        with open("encrypted_File.pdf", 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="encrypted_File.pdf"'
            response['Content-Length'] = os.path.getsize("encrypted_File.pdf")
            response['Content-Disposition'] += 'attachment; filename*=UTF-8\'\'encrypted_File.pdf'
            os.remove("encrypted_File.pdf")
            return response
    else:
        return HttpResponse("Error while downloading the file")

def download_unlocked_file(request):
    if os.path.exists("savedFile.pdf"):
        with open("savedFile.pdf", 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="savedFile.pdf"'
            response['Content-Length'] = os.path.getsize("savedFile.pdf")
            response['Content-Disposition'] += 'attachment; filename*=UTF-8\'\'savedFile.pdf'
            os.remove("savedFile.pdf")
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
   

# def download_compressed(request):
#     if os.path.exists("compressedPDF.pdf"):
#         with open("compressedPDF.pdf", 'rb') as f:
#             response = HttpResponse(f.read(), content_type='application/pdf')
#             response['Content-Disposition'] = 'attachment; filename="compressedPDF.pdf"'
#             response['Content-Length'] = os.path.getsize("compressedPDF.pdf")
#             response['Content-Disposition'] += '; attachment; filename*=UTF-8\'\'compressedPDF.pdf'
#             os.remove("compressedPDF.pdf")
#         return response    

#     elif os.path.exists("highCompressed.pdf"):
#         with open("highCompressed.pdf", 'rb') as fp:
#             response = HttpResponse(fp.read(), content_type='application/pdf')
#             response['Content-Disposition'] = 'attachment; filename="highCompressed.pdf"'
#             response['Content-Length'] = os.path.getsize("highCompressed.pdf")
#             response['Content-Disposition'] += '; attachment; filename*=UTF-8\'\'highCompressed.pdf'
#             os.remove("highCompressed.pdf")
#         return response    

#     else:
#         return HttpResponse("The compressed file does not exist.")