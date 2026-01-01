import os
from flask import Blueprint, request
from app.extensions import services
 
doc_app = Blueprint("doc", __name__, url_prefix="/doc")

@doc_app.route("/txt", methods=["POST"])
def txtPost():
    file = request.files["file"]
    dir_path = "db/txt/"
    file_name = file.filename
    save_path = dir_path + file_name
    
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    file.save(save_path)

    pdf_load_result = services.llm_service.document_loader.load_txt(save_path)

    resp = {
        "status": "success", 
        "filename": file_name,
        "size": pdf_load_result.size,
        "doc_len": pdf_load_result.doc_length,
        "chunks": pdf_load_result.chunks_length,
        "langs": pdf_load_result.lang
    }

    return resp

@doc_app.route("/pdf", methods=["POST"])
def pdfPost():
    file = request.files["file"]
    dir_path = "db/pdf/"
    file_name = file.filename
    save_path = dir_path + file_name
    
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    
    file.save(save_path)


    pdf_load_result = services.llm_service.document_loader.load_pdf(save_path)

    resp = {
        "status": "success", 
        "filename": file_name,
        "size": pdf_load_result.size,
        "doc_len": pdf_load_result.doc_length,
        "chunks": pdf_load_result.chunks_length,
        "langs": pdf_load_result.lang
    }

    return resp

@doc_app.route("/epub", methods=["POST"])
def epubPost():
    file = request.files["file"]
    dir_path = "db/epub/"    
    file_name = file.filename
    save_path = dir_path + file_name
    
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    file.save(save_path)

    pdf_load_result = services.llm_service.document_loader.load_epub(save_path)

    resp = {
        "status": "success", 
        "filename": file_name,
        "size": pdf_load_result.size,
        "doc_len": pdf_load_result.doc_length,
        "chunks": pdf_load_result.chunks_length,
        "langs": pdf_load_result.lang
    }

    return resp

@doc_app.route("/docx", methods=["POST"])
def docxPost():
    file = request.files["file"]
    dir_path = "db/docx/"
    file_name = file.filename
    save_path = dir_path + file_name

    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    file.save(save_path)

    pdf_load_result = services.llm_service.document_loader.load_docx(save_path)

    resp = {
        "status": "success", 
        "filename": file_name,
        "size": pdf_load_result.size,
        "doc_len": pdf_load_result.doc_length,
        "chunks": pdf_load_result.chunks_length,
        "langs": pdf_load_result.lang
    }

    return resp

@doc_app.route("/pptx", methods=["POST"])
def pptxPost():
    file = request.files["file"]
    dir_path = "db/pptx/"
    file_name = file.filename
    save_path = file_name + file_name

    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    file.save(save_path)

    pdf_load_result = services.llm_service.document_loader.load_pptx(save_path)

    resp = {
        "status": "success", 
        "filename": file_name,
        "size": pdf_load_result.size,
        "doc_len": pdf_load_result.doc_length,
        "chunks": pdf_load_result.chunks_length,
        "langs": pdf_load_result.lang
    }

    return resp

@doc_app.route("/md", methods=["POST"])
def mdPost():
    file = request.files["file"]
    dir_path = "db/md"
    file_name = file.filename
    save_path = dir_path + file_name

    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    file.save(save_path)

    pdf_load_result = services.llm_service.document_loader.load_md(save_path)

    resp = {
        "status": "success", 
        "filename": file_name,
        "size": pdf_load_result.size,
        "doc_len": pdf_load_result.doc_length,
        "chunks": pdf_load_result.chunks_length,
        "langs": pdf_load_result.lang
    }

    return resp

@doc_app.route("/html", methods=["POST"])
def htmlPost():
    file = request.files["file"]
    dir_path = "db/html"
    file_name = file.filename
    save_path = dir_path + file_name

    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    file.save(save_path)

    pdf_load_result = services.llm_service.document_loader.load_html(save_path)

    resp = {
        "status": "success", 
        "filename": file_name,
        "size": pdf_load_result.size,
        "doc_len": pdf_load_result.doc_length,
        "chunks": pdf_load_result.chunks_length,
        "langs": pdf_load_result.lang
    }

    return resp