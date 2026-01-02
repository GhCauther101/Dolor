from flask import Blueprint, request
from app.extensions import services
from app.services.service_utils import compose_retrieval_chain
from app.routes.routes_utils import *
import shutil
 
doc_app = Blueprint("session", __name__, url_prefix="/doc")

@doc_app.route("/ask_agent/<session_id>", methods=["GET"])
def aiSessionGET(session_id):
    json_content = request.json
    query = json_content.get("query") if json_content else None
    session_dir = "db/sessions/" + session_id

    chain = compose_retrieval_chain(
        llm=services.llm_service.llm,
        vector_store=services.llm_service.get_session_vector_store(db_path=session_dir),
        raw_prompt=services.llm_service.prompt_template
    )

    result = chain.invoke({"input" : query})

    sources = []
    for doc in result["context"]:
        sources.append({ "source": doc.metadata["source"], "page_content": doc.page_content })

    return {"response": result["answer"], "sources": sources}

@doc_app.route("/upload", methods=["DELETE"])
def sessionDELETE(session_id):
    json_content = request.json
    session_dir = "db/sessions/" + session_id

    shutil.rmtree(session_dir)
    return {
        "session_id": session_id,
        "message": "session storage deleted"
    }

@doc_app.route("/upload", methods=["POST"])
def sessionPOST():
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