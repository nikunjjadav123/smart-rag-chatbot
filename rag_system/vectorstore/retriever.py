import streamlit as st
from langchain_community.vectorstores import Chroma

from config.settings import CHROMA_DIR
from embeddings.hf_embeddings import load_embeddings

@st.cache_resource
def load_retriever():
    embeddings = load_embeddings()

    vectorstore = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )

    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )
