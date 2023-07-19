from django.contrib import admin
from django.urls import path
from pdfEditorApp.views import compressPdf, displayPdf, lockPdf, unlockPdf, addImage
from pdfEditorApp.views import homePagePdf,deletePagePdf, fillFormPdf, appendPdf, download_append_file

urlpatterns = [
    path('', homePagePdf, name='homePagePdf'),
    path('admin/', admin.site.urls),
    path('displayPdf/', displayPdf, name='displayPdf'),
    path('addImage/', addImage, name='addImage'),
    path('deletePagePdf/', deletePagePdf, name='deletePagePdf'),
    path('fillFormPdf/', fillFormPdf, name='fillFormPdf'),

    path('appendPdf/', appendPdf, name='appendPdf'),
    path('download_append_file', download_append_file, name='download_append_file'),
   

    path('compressPdf/', compressPdf, name='compressPdf'),
    path('appendPdf/', appendPdf, name='appendPdf'),
    path('download_append_file', download_append_file, name='download_append_file'),
    path('unlockPdf/', unlockPdf, name='unlockPdf'),
    path('lockPdf/', lockPdf, name='lockPdf'),
]


