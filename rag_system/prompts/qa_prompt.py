from langchain_core.prompts import PromptTemplate

QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
Rules:
- Answer ONLY the user’s question
- Use ONLY the provided context
- Give a SINGLE, concise answer
- Do NOT repeat words or names
- Do NOT list multiple questions
- If the answer is not present, say: "Answer not found in the document"


Context:
{context}

Question:
{question}

Answer:
"""
)
