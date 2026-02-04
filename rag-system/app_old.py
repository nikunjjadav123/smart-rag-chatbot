import streamlit as st
from vectorstore.retriever import load_retriever
from llm.hf_llm import load_llm
from chains.qa_chain import ask_question
from vectorstore.index_builder import rebuild_index

st.set_page_config(
    page_title="Document Intelligence Assistant",
    layout="centered"
)

st.title("📄 Document Intelligence Assistant")
st.caption("Ask questions and get accurate answers grounded in your uploaded documents")

if "qa_history" not in st.session_state:
    st.session_state.qa_history = []


retriever = load_retriever()
llm = load_llm()

# UI
question = st.text_input("Ask a question from the PDFs:")

if st.button("Get Answer"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            result = ask_question(question, retriever, llm)
            st.session_state.qa_history.append((question, result))

        st.markdown("### Answer")
        st.write(result["answer"])

        if result["pages"]:
            pages = ", ".join(f"Page {p}" for p in result["pages"])
            st.markdown(f"📄 **Source:** {pages}")



st.sidebar.title("🛠️ Admin Panel")

with st.sidebar:
    st.subheader("Index Management")

    if st.button("🔄 Reload Vector Index"):
        with st.spinner("Reloading retriever..."):
            rebuild_index()
            st.success("Vector index reloaded successfully!")

    st.divider()

    if st.button("🧹 Clear Chat History"):
        st.session_state.qa_history = []
        st.success("Chat history cleared!")

    st.divider()

    st.subheader("System Info")
    st.markdown("""
    **Vector DB:** Chroma  
    **Embedding Model:** all-MiniLM-L6-v2  
    **LLM:** TinyLlama / HF  
    """)

    st.divider()

    st.caption("Admin-only controls")

