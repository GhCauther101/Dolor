from .services.llm_service import LlmService

class Services:
    llm_service: LlmService = None

services = Services()