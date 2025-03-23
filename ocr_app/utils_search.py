import re
import faiss
from django.conf import settings
from sentence_transformers import SentenceTransformer
from .models import Document

# Initialize FAISS & SBERT
sbert_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
index = faiss.IndexFlatL2(384)  # Adjust based on SBERT embedding size
documents_db = []  # Store document IDs

def index_documents():
    """Indexes all documents using FAISS and SBERT."""
    global index, documents_db
    documents = Document.objects.all()

    texts = []
    doc_ids = []

    for doc in documents:
        if doc.extracted_text:
            texts.append(doc.extracted_text)
            doc_ids.append(doc.id)

    if not texts:
        return  # Exit if no valid documents

    embeddings = sbert_model.encode(texts, convert_to_numpy=True)

    documents_db = doc_ids  # Store document IDs
    index.add(embeddings)

def search_documents(query):
    """Searches all documents and returns matching file URLs."""
    global index, documents_db

    if index.ntotal == 0:
        index_documents()  # Rebuild FAISS index if empty

    query_lower = query.lower()
    word_pattern = rf"\b{re.escape(query_lower)}\b"

    # Retrieve all documents that match the query (not just top-k)
    matched_documents = [
        doc for doc in Document.objects.all()
        if doc.extracted_text and re.search(word_pattern, doc.extracted_text, re.IGNORECASE)
    ]

    # Return file URLs of all matched documents
    return [doc.get_file_url() for doc in matched_documents]
