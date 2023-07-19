from django.contrib import admin
from django.urls import path
from pdfEditorApp.views import download_compressed, compressPdf, displayPdf, lockPdf, unlockPdf, addImage
from pdfEditorApp.views import homePagePdf,deletePagePdf, fillFormPdf

urlpatterns = [
    path('', homePagePdf, name='homePagePdf'),
    path('admin/', admin.site.urls),
    path('displayPdf/', displayPdf, name='displayPdf'),
    path('addImage/', addImage, name='addImage'),
    path('deletePagePdf/', deletePagePdf, name='deletePagePdf'),
    path('fillFormPdf/', fillFormPdf, name='fillFormPdf'),

    path('compressPdf/', compressPdf, name='compressPdf'),
    path('download-compressed/', download_compressed, name='download_compressed'),
    path('unlockPdf/', unlockPdf, name='unlockPdf'),
    path('lockPdf/', lockPdf, name='lockPdf'),
]
