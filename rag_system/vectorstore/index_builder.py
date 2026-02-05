import os
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from config.settings import PDF_DIR, CHROMA_DIR
from embeddings.hf_embeddings import load_embeddings


def rebuild_index():

    loader = DirectoryLoader(
        str(PDF_DIR),
        glob="**/*.pdf",
        loader_cls=PyPDFLoader
    )

    documents = loader.load()

    if not documents:
        raise ValueError("No PDF files found in the directory.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    vectordb = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=load_embeddings()
    )

    vectordb.add_documents(chunks)
    vectordb.persist()

    print(f"✅ Indexed {len(chunks)} chunks")
