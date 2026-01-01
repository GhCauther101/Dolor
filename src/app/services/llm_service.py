import os
from langchain_ollama import OllamaLLM
from langchain_chroma import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.prompts import PromptTemplate
from app.services.document_loader import DocumentLoader

class LlmService:
    def __init__(self):
        db_path = os.getenv("LOCAL_DB_PATH")
        model_name = os.getenv("LOCAL_OLLAMA_MODEL")

        self.llm = OllamaLLM(model=model_name, temperature=0.4)
        self.embedding = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=20, is_separator_regex=False)
        self.document_loader = DocumentLoader(splitter=self.splitter, embedding=self.embedding, db_path=db_path)

        self.prompt_template = PromptTemplate.from_template("""
            <s>[INST] You are a technical assistant good at searching documents. If you do not have an answer from the provided information say so. [/INST]</s>
            [INST] {input}
                    Context: {context}
                    Answer:
            [/INST]
            """)
        
        self.vector_store = Chroma(persist_directory=db_path, embedding_function=self.embedding)