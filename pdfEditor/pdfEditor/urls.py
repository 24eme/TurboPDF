from django.contrib import admin
from django.urls import path
from pdfEditorApp.views import download_compressed, compressPdf, displayPdf, lockPdf, unlockPdf, addImage, appendPdf
from pdfEditorApp.views import download_locked_file, download_unlocked_file, homePagePdf, download_append_file, deletePagePdf, fillFormPdf

urlpatterns = [
    path('', homePagePdf, name='homePagePdf'),
    path('admin/', admin.site.urls),
    path('displayPdf/', displayPdf, name='displayPdf'),
    path('addImage/', addImage, name='addImage'),
    path('deletePagePdf/', deletePagePdf, name='deletePagePdf'),
    path('fillFormPdf/', fillFormPdf, name='fillFormPdf'),

    path('compressPdf/', compressPdf, name='compressPdf'),
    path('download-compressed/', download_compressed, name='download_compressed'),
    path('appendPdf/', appendPdf, name='appendPdf'),
    path('download_append_file', download_append_file, name='download_append_file'),
    path('unlockPdf/', unlockPdf, name='unlockPdf'),
    path('download_unlocked_file', download_unlocked_file, name='download_unlocked_file'),
    path('lockPdf/', lockPdf, name='lockPdf'),
    path('download_locked_file', download_locked_file, name='download_locked_file'),
]


