from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from langdetect import detect

def compose_retrieval_chain(llm: OllamaLLM, raw_prompt: str, vector_store: Chroma):
    retriever = vector_store.as_retriever(
        searcg_type="similarity_score_threshold",
        search_kwargs={
            "k": 20,
        }
    )
    
    document_chain = create_stuff_documents_chain(llm, raw_prompt)
    chain = create_retrieval_chain(retriever, document_chain)
    return chain

def get_word_doc_page_break_count(doc):
    page_breaks = 0

    for p in doc.paragraphs:
        for run in p.runs:
            if run._element.xpath('.//w:br[@w:type="page"]'):
                page_breaks += 1

    return page_breaks


def perform_lang_detect(raw):
    try:
        return detect(raw)
    except Exception:
        pass

def safe_detect_language(chunks):
    result = set()
    min_chars=20

    for chunk in chunks:
        if isinstance(chunk, str):
            result.add(perform_lang_detect(chunk))
            continue

        if chunk.page_content or len(chunk.page_content.strip()) >= min_chars:        
            result.add(perform_lang_detect(chunk.page_content))
        else: continue

    return list(result)

