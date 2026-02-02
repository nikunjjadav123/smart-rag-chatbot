from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaLLM,OllamaEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_chroma import Chroma

# --------------------------------------------------
# 1. Load PDF
# --------------------------------------------------
loader = PyPDFLoader("Monthly_Current_affairs_1_to_31_December_2025.pdf")
documents = loader.load()


# --------------------------------------------------
# 2. Split PDF into chunks
# --------------------------------------------------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)
chunks = splitter.split_documents(documents)

# --------------------------------------------------
# 3. Create embeddings
# --------------------------------------------------
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# --------------------------------------------------
# 4. Store in FAISS Vector DB
# --------------------------------------------------
# vectorstore = FAISS.from_documents(chunks, embeddings)

vectorstore = Chroma.from_documents(
    documents=chunks,
    persist_directory="./chroma_db",
    embedding=embeddings
)


# --------------------------------------------------
# 5. Create Retriever
# --------------------------------------------------
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 10}
)

# --------------------------------------------------
# 6. LLM
# --------------------------------------------------
llm = OllamaLLM(
    model="qwen2.5:1.5b",
    temperature=0.0,
    max_tokens=256
)

# --------------------------------------------------
# 7. Strong PDF-grounded Prompt
# --------------------------------------------------
prompt = PromptTemplate(
    template="""
You are answering ONLY using the provided PDF content.

Rules:
- Use ONLY the context
- Do NOT add external knowledge
- If the answer is not found, say:
  "The PDF does not mention this information."

Question:
{question}

Context:
{context}

Answer (concise, exam-friendly):
""",
    input_variables=["question", "context"]
)

parser = StrOutputParser()

# --------------------------------------------------
# 8. Ask Question (Retriever + LLM)
# --------------------------------------------------
question = "Hornbill Festival"

docs = retriever.invoke(question)

context = "\n\n".join(doc.page_content for doc in docs)

chain = prompt | llm | parser
result = chain.invoke({"question": question, "context": context})

print(result)
