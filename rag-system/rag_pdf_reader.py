import os
import streamlit as st

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# --------------------------------------------------
# Streamlit Page Config
# --------------------------------------------------
st.set_page_config(page_title="Document Intelligence Assistant", layout="centered")
st.title("📄 Document Intelligence Assistant")
st.caption("Ask questions and get accurate answers grounded in your uploaded documents")
st.caption("Note : For now, the app is using Hugging Face, so it’s a bit slow. Within a week, I’ll switch to a paid OpenAI model, and the speed will improve a lot.")


PDF_PATH = "../uploads/documents/Monthly_Current_affairs_1_to_31_December_2025.pdf"
CHROMA_DIR = "./chroma_db_hf"

if "qa_history" not in st.session_state:
    st.session_state.qa_history = []


# --------------------------------------------------
# Load & Cache RAG Pipeline
# --------------------------------------------------
@st.cache_resource
def load_rag_pipeline():
    if not os.path.exists(PDF_PATH):
        st.error(f"PDF file not found: {PDF_PATH}")
        st.stop()

    # 1. Load PDF
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    # 2. Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    chunks = splitter.split_documents(documents)

    # 3. Embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # 4. Vector Store (Chroma)
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 2}
    )

    # 5. Lightweight LLM
    model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id)

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=256,
        temperature=0.0,
        do_sample=False,
        return_full_text=False
    )

    llm = HuggingFacePipeline(pipeline=pipe)

    # 6. Prompt (context hidden from user)
    prompt = PromptTemplate(
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

    return retriever, llm, prompt

# --------------------------------------------------
# Helper: Build Clean Context
# --------------------------------------------------
def build_clean_context(docs):
    return "\n\n".join(d.page_content.strip() for d in docs)

# --------------------------------------------------
# Ask Question
# --------------------------------------------------
def ask_question(question, retriever, llm, prompt):
    
    docs = retriever.invoke(question)

    if not docs:
        return "I don't know based on the provided PDF So i am giving an answer from my knowledge"

    context = build_clean_context(docs)

    if not context.strip():
        return "I don't know based on the provided PDF So i am giving an answer from my knowledge"

    chain = prompt | llm | StrOutputParser()

    response = chain.invoke({
        "question": question,
        "context": context
    })

    return response

# --------------------------------------------------
# Streamlit UI Logic
# --------------------------------------------------
retriever, llm, prompt = load_rag_pipeline()

question = st.text_input("Ask a question from the PDF:")

if st.button("Get Answer"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            answer = ask_question(question, retriever, llm, prompt)

        st.session_state.qa_history.append((question, answer))

# Display history ONCE
for q, a in st.session_state.qa_history:
    st.markdown(f"**Question:** {q}")
    st.markdown(f"**Answer:** {a}")
    st.markdown("---")

