from dotenv import load_dotenv
from flask import Flask
from .extensions import services
from .services.llm_service import LlmService 
from app.routes.doc_routes import doc_app
from app.routes.ai_routes import ai_app

def create_app():
    load_dotenv()
    app = Flask(__name__)

    services.llm_service = LlmService()

    app.register_blueprint(doc_app)
    app.register_blueprint(ai_app)

    return app