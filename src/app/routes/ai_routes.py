from flask import Blueprint, request
from app.extensions import services
from app.services.service_utils import compose_retrieval_chain

ai_app = Blueprint("ai", __name__, url_prefix="/ai")

@ai_app.route("/ask_pdf", methods=["POST"])
def aiPost():
    print("Post /ask_pdf called")
    json_content = request.json
    query = json_content.get("query")

    print(f"query: {query}")
    chain = compose_retrieval_chain(
        llm=services.llm_service.llm,
        raw_prompt=services.llm_service.prompt_template,
        vector_store=services.llm_service.vector_store
    )

    result = chain.invoke({"input" : query})

    sources = []
    for doc in result["context"]:
        sources.append({ "source":doc.metadata["source"], "page_content": doc.page_content })

    return {"response": result["answer"], "sources": sources}