from django.contrib import admin
from django.urls import path
from pdfEditorApp.views import download_compressed, compressPdf, displayPdf, lockPdf, unlockPdf, addImage
from pdfEditorApp.views import fillFormPdf, appendPdf, download_append_file, splitPdf
from pdfEditorApp.views import homePagePdf,deletePagePdf,pdfToImage, modifyText



urlpatterns = [
    path('', homePagePdf, name='homePagePdf'),
    path('admin/', admin.site.urls),
    path('displayPdf/', displayPdf, name='displayPdf'),
    path('addImage/', addImage, name='addImage'),
    path('deletePagePdf/', deletePagePdf, name='deletePagePdf'),
    path('fillFormPdf/', fillFormPdf, name='fillFormPdf'),

    path('appendPdf/', appendPdf, name='appendPdf'),
    path('download_append_file', download_append_file, name='download_append_file'),
     path('pdfToImage/', pdfToImage, name='pdfToImage'),
    path('download_compressed', download_compressed, name='download_compressed'),
   

    path('compressPdf/', compressPdf, name='compressPdf'),
    path('appendPdf/', appendPdf, name='appendPdf'),
    path('download_append_file', download_append_file, name='download_append_file'),
    path('unlockPdf/', unlockPdf, name='unlockPdf'),
    path('lockPdf/', lockPdf, name='lockPdf'),
    path('splitPdf/', splitPdf, name='splitPdf'),
    path('modifyText/', modifyText, name='modifyText'),
]


