import os

# config/settings.py → go up one level to rag_system
BASE_DIR_FOR_CHROMA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR_FOR_PDF = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PDF_DIR = os.path.join(BASE_DIR_FOR_PDF, "uploads", "documents")
CHROMA_DIR = os.path.join(BASE_DIR_FOR_CHROMA, "chroma_db_new")

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
