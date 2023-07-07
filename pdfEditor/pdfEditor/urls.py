
from django.contrib import admin
from django.urls import path
from pdfEditorApp.views import download_compressed, compressPdf, displayPdf, lockPdf, unlockPdf, addImage
from pdfEditorApp.views import download_locked_file, download_unlocked_file, homePagePdf

urlpatterns = [
    path('', homePagePdf, name='homePagePdf'),
    path('compressPdf/', compressPdf, name='compressPdf'),
    path('admin/', admin.site.urls),
    path('download-compressed/', download_compressed, name='download_compressed'),

    path('displayPdf/', displayPdf, name='displayPdf'),
    path('lockPdf/', lockPdf, name='lockPdf'),

    path('unlockPdf/', unlockPdf, name='unlockPdf'),
    path('download_unlocked_file', download_unlocked_file, name='download_unlocked_file'),

    path('download_locked_file', download_locked_file, name='download_locked_file'),
    path('addImage/', addImage, name='addImage'),
]
