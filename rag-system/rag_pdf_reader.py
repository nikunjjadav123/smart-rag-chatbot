import os
import streamlit as st

from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# --------------------------------------------------
# Config
# --------------------------------------------------
PDF_DIR = "../uploads/documents"
CHROMA_DIR = "./chroma_db_hf"

st.set_page_config(page_title="Document Intelligence Assistant", layout="centered")
st.title("📄 Document Intelligence Assistant")
st.caption("Ask questions and get accurate answers grounded in your uploaded documents")

# --------------------------------------------------
# Embedding Model (load once)
# --------------------------------------------------
@st.cache_resource
def load_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

# --------------------------------------------------
# Rebuild Vector Index (BATCH EMBEDDING)
# --------------------------------------------------
def rebuild_index():
    if not os.path.exists(PDF_DIR):
        st.error(f"PDF directory not found: {PDF_DIR}")
        return

    loader = DirectoryLoader(
        PDF_DIR,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader
    )
    documents = loader.load()

    if not documents:
        st.warning("No PDF files found to index.")
        return

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)

    embeddings = load_embeddings()

    # 🔥 Rebuild Chroma from scratch
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )

# --------------------------------------------------
# Load Retriever (NO EMBEDDING HERE)
# --------------------------------------------------
@st.cache_resource
def load_retriever():
    embeddings = load_embeddings()

    vectorstore = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )

    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}  # 👈 important for multi-PDF
    )

# --------------------------------------------------
# Load LLM
# --------------------------------------------------
@st.cache_resource
def load_llm():
    model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id)

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=256,
        temperature=0.4,
        do_sample=False,
        return_full_text=False
    )

    return HuggingFacePipeline(pipeline=pipe)

# --------------------------------------------------
# Prompt
# --------------------------------------------------
PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
Answer the question using ONLY the internal information.
If the information is not present, say:
"The PDF does not mention this information."

Context:
{context}

Question:
{question}

Answer:
"""
)

# --------------------------------------------------
# Helper
# --------------------------------------------------
def build_context(docs):
    return "\n\n".join(d.page_content for d in docs)

# --------------------------------------------------
# Ask Question
# --------------------------------------------------
def ask_question(question, retriever, llm):
    docs = retriever.invoke(question)

    if not docs:
        return "The PDF does not mention this information."

    context = build_context(docs)

    chain = PROMPT | llm | StrOutputParser()
    return chain.invoke({"context": context, "question": question})

# --------------------------------------------------
# Sidebar (Admin Controls)
# --------------------------------------------------
st.sidebar.title("Admin")

if st.sidebar.button("🔁 Rebuild Knowledge Index"):
    with st.spinner("Rebuilding vector index..."):
        rebuild_index()
        load_retriever.clear()  # IMPORTANT
    st.sidebar.success("Index rebuilt successfully")

# --------------------------------------------------
# Main UI
# --------------------------------------------------
retriever = load_retriever()
llm = load_llm()

question = st.text_input("Ask a question from the PDFs:")

if st.button("Get Answer"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            answer = ask_question(question, retriever, llm)

        st.markdown("### Answer")
        st.write(answer)
