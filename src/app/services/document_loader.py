import os
from langchain_chroma import Chroma
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document as LcDocument
from langchain_community.document_loaders import UnstructuredHTMLLoader, UnstructuredEPubLoader
from pptx import Presentation
from docx import Document
from app.services.service_utils import get_word_doc_page_break_count

class DocumentLoadResult:
    def __init__(self, extension, size, doc_length, chunks_length):
        self.extension = extension
        self.size = size
        self.doc_length = doc_length
        self.chunks_length = chunks_length

class DocumentLoader:
    def __init__(self, splitter, embedding, db_path):
        self.text_splitter = splitter
        self.embedding = embedding
        self.db_path = db_path

    def load_txt(self, path) -> DocumentLoadResult:
        txt = None
        with open(path, "r+") as f:
            txt = f.read()

        size_bytes = os.path.getsize(path)
        chunks = self.text_splitter.split_text(txt)

        vector_store = Chroma.from_texts(chunks=chunks, embedding=self.embedding, persist_directory=self.db_path)
        # vector_store.persist()

        return DocumentLoadResult(extension='txt', size=size_bytes, chunks_length=len(chunks))

    def load_pdf(self, path) -> DocumentLoadResult:
        size_bytes = os.path.getsize(path)
        pdf_loader = PDFPlumberLoader(path)
        docs = pdf_loader.load_and_split()
        chunks = self.text_splitter.split_documents(docs)
        
        vector_store = Chroma.from_documents(documents=chunks, embedding=self.embedding, persist_directory=self.db_path)
        # vector_store.persist()

        return DocumentLoadResult(extension='pdf', size=size_bytes, doc_length=len(docs), chunks_length=len(chunks))

    def load_epub(self, path) -> DocumentLoadResult:
        size_bytes = os.path.getsize(path)
        epub_loader = UnstructuredEPubLoader(path)
        docs = epub_loader.load()
        chunks = self.text_splitter.split_documents(docs)

        vector_store = Chroma.from_documents(documents=chunks, embedding=self.embedding, persist_directory=self.db_path)
        # vector_store.persist()
        
        return DocumentLoadResult(extension='epub', size=size_bytes, doc_length=len(docs), chunks_length=len(chunks))

    def load_docx(self, path) -> DocumentLoadResult:
        size_bytes = os.path.getsize(path)
        document = python_docs.Document(path)
        page_count = get_word_doc_page_break_count(document)
        text = '\n'.join([pr.text for pr in document.paragraphs if pr.text.strip()])
        chunks = self.text_splitter.split_text(text)

        vector_store = Chroma.from_documents(documents=chunks, embedding=self.embedding, persist_directory=self.db_path)
        # vector_store.persist()

        return DocumentLoadResult(extension='docx', size=size_bytes, doc_length=page_count, chunks_length=len(chunks))

    def load_pptx(self, path) -> DocumentLoadResult:
        size_bytes = os.path.getsize(path)
        presentation = Presentation(path)
        documents = []

        for sld_num, sld in enumerate(presentation.slides, start=1):
            slide_text = []
            for shape in sld.shapes:
                if not shape.has_text_frame:
                    continue
                 
                for prg in shape.text_frame.paragraphs:
                    text = prg.text.strip()
                    if text:
                        slide_text.appen(text)
            
            if slide_text:
                documents.append(
                    LcDocument( 
                        page_content="\n".join(slide_text),
                        metadata={
                            "slide": sld_num,
                            "type": "pptx"}
                ))

        chunks = self.text_splitter.split_documents(documents=documents)
        vector_store = Chroma.from_documents(documents=chunks, embedding=self.embedding, persist_directory=self.db_path)
        # vector_store.persist()

        return DocumentLoadResult(extension='pptx', size=size_bytes, doc_length=len(sld), chunks_length=len(chunks))

    def load_md(self, path):
        size_bytes = os.path.getsize(path)
        loader = TextLoader(path, encoding="utf-8")
        docs = loader.load_and_split()
        chunks = self.text_splitter.split_documents(docs)

        vector_store = Chroma.from_documents(documents=chunks, embedding=self.embedding, persist_directory=self.db_path)
        # vector_store.persist()
        
        return DocumentLoadResult(extension='md', size=size_bytes, doc_length=len(docs), chunks_length=len(chunks))

    def load_html(self, path):
        size_bytes = os.path.getsize(path)
        loader = UnstructuredHTMLLoader(path)
        docs = loader.load()
        chunks = self.text_splitter.split_documents(documents=docs)
        vector_store = Chroma.from_documents(documents=chunks, embedding=self.embedding, persist_directory=self.db_path)
        # vector_store.persist()

        return DocumentLoadResult(extension='html', size=size_bytes, doc_length=len(docs), chunks_length=len(chunks))