from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from .models import Document
from .utils_ocr import extract_text_from_image, extract_text_from_pdf, extract_text_from_word
from .utils_search import search_documents
import os 
from django.conf import settings

class UploadDocumentView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        if 'file' not in request.FILES:
            return Response({"error": "No file uploaded"}, status=400)

        file = request.FILES['file']
        
        # Save file and get full absolute path
        relative_file_path = default_storage.save(f"documents/{file.name}", file)
        file_path = os.path.join(settings.MEDIA_ROOT, relative_file_path)

        # Process based on file type
        if file.name.endswith(".pdf"):
            extracted_text = extract_text_from_pdf(file_path)
        elif file.name.endswith(".docx"):
            extracted_text = extract_text_from_word(file_path)
        else:
            extracted_text = extract_text_from_image(file_path)

        # Save document record in the database
        document = Document.objects.create(file=relative_file_path, extracted_text=extracted_text)

        return Response({"message": "File uploaded", "text": extracted_text}, status=201)
class SearchDocumentView(APIView):
        def get(self, request):
            query = request.GET.get("query", "")
            if not query:
                return Response({"error": "Query parameter is required"}, status=400)

            results = search_documents(query)
            return Response({"results": results})   