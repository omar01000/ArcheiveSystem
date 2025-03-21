from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from .models import Document

sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.IndexFlatL2(384)  
documents_db = [] 
def index_documents():
    global index, documents_db
    documents = Document.objects.all()

    # Avoid empty document indexing
    texts = [doc.extracted_text for doc in documents if doc.extracted_text]

    if not texts:
        return  # Avoid indexing an empty list

    embeddings = sbert_model.encode(texts, convert_to_numpy=True)

    documents_db.extend(texts)
    index.add(embeddings)

def search_documents(query, top_k=5):
    if index.ntotal == 0:
        index_documents()  # Rebuild FAISS index if empty

    query_embedding = sbert_model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)

    results = [documents_db[idx] for idx in indices[0] if 0 <= idx < len(documents_db)]
    return results
