
from django.contrib import admin
from django.urls import path
from pdfEditorApp.views import download_compressed, compressPdf


urlpatterns = [
    path('', compressPdf, name='compressPdf'),
    path('admin/', admin.site.urls),
    path('download-compressed/', download_compressed, name='download_compressed'),
]
