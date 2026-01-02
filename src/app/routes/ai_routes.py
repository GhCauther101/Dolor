from flask import Blueprint, request, render_template
from app.extensions import services
from app.services.service_utils import compose_retrieval_chain
from app.routes.routes_utils import *

ai_app = Blueprint("global", __name__, url_prefix="/ai")

@ai_app.route("/")
def home():
    return render_template("home.html")

@ai_app.route("/ask_agent", methods=["POST"])
def aiPOST():
    json_content = request.json
    query = json_content.get("query")

    chain = compose_retrieval_chain(
        llm=services.llm_service.llm,
        vector_store=services.llm_service.vector_store,
        raw_prompt=services.llm_service.prompt_template
    )

    result = chain.invoke({"input" : query})

    sources = []
    for doc in result["context"]:
        sources.append({ "source": doc.metadata["source"], "page_content": doc.page_content })

    return {"response": result["answer"], "sources": sources}

@ai_app.route("/upload_txt", methods=["POST"])
def txtPost():
    dir_path = "db/txt/"
    file = extract_file(request_object=request)
    save_path = process_file(dir_path=dir_path, filename=file.filename)
    pdf_load_result = services.llm_service.document_loader.load_txt(save_path)

    resp = {
        "status": "success", 
        "filename": file.filename,
        "size": pdf_load_result.size,
        "doc_len": pdf_load_result.doc_length,
        "chunks": pdf_load_result.chunks_length,
        "langs": pdf_load_result.lang
    }

    return resp

@ai_app.route("/upload_pdf", methods=["POST"])
def pdfPost():
    file = extract_file(request_object=request)
    dir_path = "db/pdf/"
    save_path = process_file(dir_path=dir_path, filename=file.filename)
    pdf_load_result = services.llm_service.document_loader.load_pdf(save_path)

    resp = {
        "status": "success", 
        "filename": file.filename,
        "size": pdf_load_result.size,
        "doc_len": pdf_load_result.doc_length,
        "chunks": pdf_load_result.chunks_length,
        "langs": pdf_load_result.lang
    }

    return resp

@ai_app.route("/upload_epub", methods=["POST"])
def epubPost():
    file = extract_file(request_object=request)
    dir_path = "db/epub/"    
    save_path = process_file(dir_path=dir_path, filename=file.filename)
    pdf_load_result = services.llm_service.document_loader.load_epub(save_path)

    resp = {
        "status": "success", 
        "filename": file.filename,
        "size": pdf_load_result.size,
        "doc_len": pdf_load_result.doc_length,
        "chunks": pdf_load_result.chunks_length,
        "langs": pdf_load_result.lang
    }

    return resp

@ai_app.route("/upload_docx", methods=["POST"])
def docxPost():
    file = extract_file(request_object=request)
    dir_path = "db/docx/"
    save_path = process_file(dir_path=dir_path, filename=file.filename)
    pdf_load_result = services.llm_service.document_loader.load_docx(save_path)

    resp = {
        "status": "success", 
        "filename": file.filename,
        "size": pdf_load_result.size,
        "doc_len": pdf_load_result.doc_length,
        "chunks": pdf_load_result.chunks_length,
        "langs": pdf_load_result.lang
    }

    return resp

@ai_app.route("/upload_pptx", methods=["POST"])
def pptxPost():
    file = extract_file(request_object=request)
    dir_path = "db/pptx/"
    save_path = process_file(dir_path=dir_path, filename=file.filename)
    pdf_load_result = services.llm_service.document_loader.load_pptx(save_path)

    resp = {
        "status": "success", 
        "filename": file.filename,
        "size": pdf_load_result.size,
        "doc_len": pdf_load_result.doc_length,
        "chunks": pdf_load_result.chunks_length,
        "langs": pdf_load_result.lang
    }

    return resp

@ai_app.route("/upload_md", methods=["POST"])
def mdPost():
    file = extract_file(request_object=request)
    dir_path = "db/md/"
    save_path = process_file(dir_path=dir_path, filename=file.filename)
    pdf_load_result = services.llm_service.document_loader.load_md(save_path)

    resp = {
        "status": "success", 
        "filename": file.filename,
        "size": pdf_load_result.size,
        "doc_len": pdf_load_result.doc_length,
        "chunks": pdf_load_result.chunks_length,
        "langs": pdf_load_result.lang
    }

    return resp

@ai_app.route("/upload_html", methods=["POST"])
def htmlPost():
    file = extract_file(request_object=request)
    dir_path = "db/html/"
    save_path = process_file(dir_path=dir_path, filename=file.filename)
    pdf_load_result = services.llm_service.document_loader.load_html(save_path)

    resp = {
        "status": "success", 
        "filename": file.filename,
        "size": pdf_load_result.size,
        "doc_len": pdf_load_result.doc_length,
        "chunks": pdf_load_result.chunks_length,
        "langs": pdf_load_result.lang
    }

    return resp