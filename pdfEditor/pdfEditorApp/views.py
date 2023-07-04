from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from pdfEditorApp.listing.forms import inputForm
from pdfEditorApp.compressPdf import compressPdfFunction
import os


# Create your views here.
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
            response['Content-Disposition'] += '; attachment; filename*=UTF-8\'\'compressed.pdf'

            return response
    else:
        return HttpResponse("The compressed file does not exist.")
