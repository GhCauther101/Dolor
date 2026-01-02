import os
import json
import uuid
from app.extensions import services

def extract_json(request_object):
    retreived_param = request_object.form.get("json")
    if retreived_param:
        return json.loads(retreived_param)
    else:
        return None

def extract_file(request_object):
    return request_object.files.getlist("file")

def extract_files(request_object):
    return request_object.files.getlist("files")

def process_file(dir_path, filename):
    save_path = dir_path + filename
    if dir_path:os.makedirs(dir_path, exist_ok=True)

    filename.save(save_path)
    return save_path

def create_session_folder():
    session_id = str(uuid.uuid4()).replace('-', '_')
    session_dir = "db/sessions/" + session_id + '/'
    os.makedirs(session_dir, exist_ok=True)
    return session_id, session_dir

def process_session_load(session_dir, session_files):
    session_load_results = []

    # initialize session based chroma db store
    for file in session_files:
        file_name = file.filename
        name_parts = file_name.rsplit(".", 1)
        extension = name_parts[1].lower() if len(name_parts) == 2 else ""
        save_path = session_dir + file_name
        file.save(save_path)
        
        if extension == "":
            raise Exception("could not identify file extension")

        load_result = None
        if extension == "txt":
            load_result = services.llm_service.document_loader.load_txt_session(path=save_path, file=file, session_db_path=session_dir)
        elif extension == "pdf":
            load_result = services.llm_service.document_loader.load_pdf_session(path=save_path, file=file, session_db_path=session_dir)
        elif extension == "epub":
            load_result = services.llm_service.document_loader.load_epub_session(path=save_path, file=file, session_db_path=session_dir)
        elif extension == "docx":
            load_result = services.llm_service.document_loader.load_docx_session(path=save_path, file=file, session_db_path=session_dir)
        elif extension == "pptx":
            load_result = services.llm_service.document_loader.load_pptx_session(path=save_path, file=file, session_db_path=session_dir)
        elif extension == "md":
            load_result = services.llm_service.document_loader.load_md_session(path=save_path, file=file, session_db_path=session_dir)
        elif extension == "html":
            load_result = services.llm_service.document_loader.load_html_session(path=save_path, file=file, session_db_path=session_dir)
    
        if load_result != None:
            session_load_results.append(load_result)
    
    return session_load_results
