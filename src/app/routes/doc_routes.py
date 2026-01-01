from flask import Blueprint, request
from app.extensions import services
 
doc_app = Blueprint("doc", __name__, url_prefix="/doc")
llm_service_instance = services.llm_service

@doc_app.route("/pdf", methods=["POST"])
def pdfPost():
    file = request.files["file"]
    file_name = file.filename
    save_path = "db/pdf/" + file_name
    file.save(save_path)

    pdf_load_result = services.llm_service.document_loader.load_pdf(save_path)

    resp = {
        "status": "success", 
        "filename": file_name,
        "size": pdf_load_result.size,
        "doc_len":pdf_load_result.doc_length,
        "chunks": pdf_load_result.chunks_length
    }

    return resp