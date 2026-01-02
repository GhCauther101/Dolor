from flask import Blueprint, request
from app.extensions import services
from app.services.service_utils import compose_retrieval_chain

ai_app = Blueprint("ai", __name__, url_prefix="/ai")

@ai_app.route("/ask_pdf", methods=["POST"])
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

@ai_app.route("/session/<session_id>", methods=["GET"])
def aiSessionGET(session_id):
    # json_content = request.get_json(force=True)
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