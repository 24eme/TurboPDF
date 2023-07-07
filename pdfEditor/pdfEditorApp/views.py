from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from pdfEditorApp.listing.forms import inputForm
from pdfEditorApp.compressPdf import compressPdfFunction
from pdfEditorApp.compressPdf import highCompressionPdfFunction
import os


# Create your views here.
def compressPdf(request):
    compressedFileSize = None
    form = inputForm()
    if 'filename' in request.POST:
        compressedFileSize = compressPdfFunction(request.FILES['pdf_file'])
        print('your file was compressed ', compressedFileSize)

    elif 'high-compression' in request.POST:
        compressedFileSize = highCompressionPdfFunction(request.FILES['pdf_file'])
        print('your file was highly compressed', compressedFileSize)

    else:
        form = inputForm()
    return render(request, 'compressPdf.html', {'compressedFileSize': compressedFileSize})


def download_compressed(request):
    if os.path.exists("compressedPDF.pdf"):
        print('exists')
        with open("compressedPDF.pdf", 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="compressedPDF.pdf"'
            response['Content-Length'] = os.path.getsize("compressedPDF.pdf")
            response['Content-Disposition'] += '; attachment; filename*=UTF-8\'\'compressedPDF.pdf'
            os.remove("compressedPDF.pdf")
        return response    

            
    elif os.path.exists("highCompressed.pdf"):
        print('exists high')
        with open("highCompressed.pdf", 'rb') as fp:
            response = HttpResponse(fp.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="highCompressed.pdf"'
            response['Content-Length'] = os.path.getsize("highCompressed.pdf")
            response['Content-Disposition'] += '; attachment; filename*=UTF-8\'\'highCompressed.pdf'
            os.remove("highCompressed.pdf")
        return response    

    else:
        return HttpResponse("The compressed file does not exist.")