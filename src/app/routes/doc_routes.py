import os
import json
import uuid
from flask import Blueprint, request
from app.extensions import services
from app.routes.routes_utils import *
 
doc_app = Blueprint("doc", __name__, url_prefix="/doc")

@doc_app.route("/session", methods=["POST"])
def sessionPost():
    data = extract_json(request_object=request)
    upload_files = extract_files(request_object=request)
    session_id, session_dir = create_session_folder()
    merge = data["merge"]

    session_load_result = process_session_load(
        session_dir=session_dir,
        session_files=upload_files
    )

    # merge if need
    if merge:
        print("perform global merge")

    # perform response process
    resp = {
        "session_id": session_id,
        "items": []
    }

    for load_result in session_load_result:
        resp["items"].append({
            "status": "success",
            "filename": load_result.file.filename,
            "size": load_result.size,
            "doc_len": load_result.doc_length,
            "chunks": load_result.chunks_length,
            "langs": load_result.lang
        })

    return resp

@doc_app.route("/txt", methods=["POST"])
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

@doc_app.route("/pdf", methods=["POST"])
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

@doc_app.route("/epub", methods=["POST"])
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

@doc_app.route("/docx", methods=["POST"])
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

@doc_app.route("/pptx", methods=["POST"])
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

@doc_app.route("/md", methods=["POST"])
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

@doc_app.route("/html", methods=["POST"])
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