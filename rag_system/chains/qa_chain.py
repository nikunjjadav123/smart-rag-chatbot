from langchain_core.output_parsers import StrOutputParser
from prompts.qa_prompt import QA_PROMPT
from utils.helpers import build_context,extract_page_numbers

def ask_question(question, retriever, llm):
    docs = retriever.invoke(question)

    if not docs:
        return {
            "answer": "The PDF does not mention this information.",
            "pages": []
        }

    context = build_context(docs)
    
    if not context.strip():
        return {
            "answer": "The PDF does not mention this information.",
            "pages": []
        }
    pages = extract_page_numbers(docs)
    
    chain = QA_PROMPT | llm | StrOutputParser()

    answer = chain.invoke({
        "question": question,
        "context": context
    })
    
    return {
        "answer": answer,
        "pages": pages
    }
