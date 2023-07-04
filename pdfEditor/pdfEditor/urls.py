
from django.contrib import admin
from django.urls import path
from pdfEditorApp.views import compressPdf

urlpatterns = [
     path('', compressPdf, name='compressPdf'),
    path('admin/', admin.site.urls),
]
