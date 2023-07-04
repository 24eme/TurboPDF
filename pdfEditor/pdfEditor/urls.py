
from django.contrib import admin
from django.urls import path
<<<<<<< Updated upstream
from pdfEditorApp.views import download_compressed, compressPdf, displayPdf
=======
from pdfEditorApp.views import download_compressed, compressPdf, lockPdf
from pdfEditorApp.views import download_locked_file
>>>>>>> Stashed changes

urlpatterns = [
    path('', compressPdf, name='compressPdf'),
    path('admin/', admin.site.urls),
    path('download-compressed/', download_compressed, name='download_compressed'),
<<<<<<< Updated upstream
    path('displayPdf/', displayPdf, name='displayPdf'),
=======
    path('lockPdf/', lockPdf, name='lockPdf'),
    path('download_locked_file', download_locked_file, name='download_locked_file')
>>>>>>> Stashed changes
]
