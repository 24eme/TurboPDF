from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from pdfEditorApp.listing.forms import inputForm
from pdfEditorApp.compressPdf import compressPdfFunction
import os


# Create your views here.
def compressPdf(request):

    form = inputForm()
    if request.method == 'POST':
        compressedFile = compressPdfFunction(request.FILES['pdf_file'])
        print('your file was compressed ',compressedFile)
    else :
        form = inputForm()
    return render(request, 'compressPdf.html', {'form': form})
 

