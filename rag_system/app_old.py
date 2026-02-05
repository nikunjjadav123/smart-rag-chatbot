import streamlit as st
from vectorstore.retriever import load_retriever
from llm.hf_llm import load_llm
from chains.qa_chain import ask_question
from vectorstore.index_builder import rebuild_index

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Document Intelligence Assistant",
    layout="centered"
)

st.title("📄 Document Intelligence Assistant")
st.caption("Ask questions and get accurate answers grounded in your uploaded documents")

# --------------------------------------------------
# Session State Initialization
# --------------------------------------------------
if "qa_history" not in st.session_state:
    st.session_state.qa_history = []

# --------------------------------------------------
# Load Retriever & LLM
# --------------------------------------------------
retriever = load_retriever()
llm = load_llm()

# --------------------------------------------------
# Ask Question Form (CORRECT)
# --------------------------------------------------
with st.form("qa_form"):
    question = st.text_input("Ask a question from the PDFs:")
    submit = st.form_submit_button("Get Answer")

if submit:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        # Prevent duplicate questions
        if any(q == question for q, _ in st.session_state.qa_history):
            st.warning("This question was already answered.")
        else:
            with st.spinner("Thinking..."):
                result = ask_question(question, retriever, llm)
                st.session_state.qa_history.append((question, result))

# --------------------------------------------------
# Display Latest Answer
# --------------------------------------------------
if st.session_state.qa_history:
    last_question, last_result = st.session_state.qa_history[-1]

    st.markdown("### Answer")
    st.write(last_result["answer"])

    if last_result.get("pages"):
        pages = ", ".join(f"Page {p}" for p in last_result["pages"])
        st.markdown(f"📄 **Source:** {pages}")

# --------------------------------------------------
# Sidebar Admin Panel
# --------------------------------------------------
# st.sidebar.title("🛠️ Admin Panel")

# with st.sidebar:
#     st.subheader("Index Management")

#     if st.button("🔄 Reload Vector Index"):
#         with st.spinner("Reloading vector index..."):
#             rebuild_index()
#             st.success("Vector index reloaded successfully!")

#     st.divider()

#     if st.button("🧹 Clear Chat History"):
#         st.session_state.qa_history = []
#         st.success("Chat history cleared!")

#     st.divider()

#     st.subheader("System Info")
#     st.markdown("""
#     **Vector DB:** Chroma  
#     **Embedding Model:** all-MiniLM-L6-v2  
#     **LLM:** TinyLlama (Hugging Face)  
#     """)

#     st.divider()
#     st.caption("Admin-only controls")
