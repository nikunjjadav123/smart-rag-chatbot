def build_context(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def extract_page_numbers(docs):
    pages = set()
    for doc in docs:
        if "page" in doc.metadata:
            pages.add(doc.metadata["page"] + 1)
    return sorted(pages)
