from langchain_core.prompts import PromptTemplate

QA_PROMPT = PromptTemplate(
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
