from django.urls import path
from .views import UploadDocumentView, SearchDocumentView

urlpatterns = [
    path('upload/', UploadDocumentView.as_view(), name='upload_document'),
    path('search/', SearchDocumentView.as_view(), name='search_document'),
]