import streamlit as st

from vectorstore.index_builder import rebuild_index
from vectorstore.retriever import load_retriever
from llm.hf_llm import load_llm
from chains.qa_chain import ask_question

st.set_page_config(
    page_title="Document Intelligence Assistant",
    layout="centered"
)

st.title("📄 Document Intelligence Assistant")
st.caption("Ask questions and get accurate answers grounded in your uploaded documents")

# Sidebar
st.sidebar.title("Admin")

if st.sidebar.button("🔁 Rebuild Knowledge Index"):
    with st.spinner("Rebuilding vector index..."):
        rebuild_index()
        load_retriever.clear()
    st.sidebar.success("Index rebuilt successfully")

# Load core components
retriever = load_retriever()
llm = load_llm()

# UI
question = st.text_input("Ask a question from the PDFs:")

if st.button("Get Answer"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            answer = ask_question(question, retriever, llm)

        st.markdown("### Answer")
        st.write(answer)
