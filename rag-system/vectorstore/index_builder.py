import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from config.settings import PDF_DIR, CHROMA_DIR
from embeddings.hf_embeddings import load_embeddings

def rebuild_index():
    if not os.path.exists(PDF_DIR):
        raise FileNotFoundError(f"PDF directory not found: {PDF_DIR}")

    loader = DirectoryLoader(
        PDF_DIR,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader
    )

    documents = loader.load()
    if not documents:
        raise ValueError("No PDF files found.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)
    embeddings = load_embeddings()

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )
