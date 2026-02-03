from langchain_core.output_parsers import StrOutputParser
from prompts.qa_prompt import QA_PROMPT
from utils.helpers import build_context

def ask_question(question, retriever, llm):
    docs = retriever.invoke(question)

    if not docs:
        return "The PDF does not mention this information."

    context = build_context(docs)
    chain = QA_PROMPT | llm | StrOutputParser()

    return chain.invoke({
        "context": context,
        "question": question
    })
