from django.contrib import admin
from django.urls import path
from pdfEditorApp.views import compressPdf, download_compressed, displayPdf, lockPdf, unlockPdf, addImage
from pdfEditorApp.views import fillFormPdf, appendPdf, download_append_file, splitPdf,extractPagesToPng
from pdfEditorApp.views import homePagePdf, deletePagePdf, pdfToImage, modifyText, redact, download_pdf



urlpatterns = [
    path('', homePagePdf, name='homePagePdf'),
    path('admin/', admin.site.urls),
    path('displayPdf/', displayPdf, name='displayPdf'),
    path('addImage/', addImage, name='addImage'),
    path('deletePagePdf/', deletePagePdf, name='deletePagePdf'),
    path('fillFormPdf/', fillFormPdf, name='fillFormPdf'),

    path('appendPdf/', appendPdf, name='appendPdf'),
    path('download_append_file', download_append_file, name='download_append_file'),
    path('download_compressed', download_compressed, name='download_compressed'),
    path('extractPagesToPng/', extractPagesToPng, name='extractPagesToPng'),
    path('pdfToImage/', pdfToImage, name='pdfToImage'),   

    path('compressPdf/', compressPdf, name='compressPdf'),
    path('appendPdf/', appendPdf, name='appendPdf'),
    path('download_append_file', download_append_file, name='download_append_file'),
    path('unlockPdf/', unlockPdf, name='unlockPdf'),
    path('lockPdf/', lockPdf, name='lockPdf'),
    path('splitPdf/', splitPdf, name='splitPdf'),
    path('modifyText/', modifyText, name='modifyText'),
    path('redact/', redact, name='redact'),
    path('download_pdf/<str:fichier_finale>/<str:pdf_name>/', download_pdf, name='download_pdf')
    
]


