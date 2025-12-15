from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Depends, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uuid
import os
from typing import Optional

from src.routers.models.post_request import PostRequest
from src.data_store import data_store
from src.utils.pdf_processor import extract_text_from_pdf
from src.utils.llm_client import get_llm_response
from src.services.jwt_service import verify_access_token
from src.utils.filename_sanitizer import sanitize_filename
from src.utils.uuid_utils import generate_uuid

router = APIRouter()

UPLOAD_DIR = "/tmp/cag_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ----------------------------
# Security Scheme
# ----------------------------
security = HTTPBearer()


# ----------------------------
# JWT Dependency - WORKING VERSION
# ----------------------------
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Extracts and verifies JWT token from Authorization header.
    This makes Swagger's "Authorize" button work properly.
    """
    token = credentials.credentials
    payload = verify_access_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=401, 
            detail="Invalid or expired token"
        )
    
    return payload


# ----------------------------
# 1) Generate UUID (Public - No Auth Required)
# ----------------------------
@router.get("/take_uuid")
async def get_uuid_for_data():
    """Generate a new UUID for data operations."""
    new_uuid = generate_uuid()
    return {
        "message": "Copy this UUID and use it for upload/update/query operations.",
        "uuid": new_uuid
    }


# ----------------------------
# 2) Upload PDF (JWT Protected)
# ----------------------------
@router.post("/upload/{uuid}", status_code=201)
async def upload_pdf(
    uuid: uuid.UUID,
    file: UploadFile = File(...),
    file_name: Optional[str] = Form(None),
    date: Optional[str] = Form(None),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload a PDF file and extract its text.
    Requires JWT authentication via Bearer token.
    """
    post_request = PostRequest(
        file_name=file_name,
        date=date
    )

    uuid_str = str(uuid)
    
    if file.content_type != "application/pdf":
        raise HTTPException(400, "Invalid file type. Only PDF files are accepted.")

    if uuid_str in data_store:
        raise HTTPException(
            400, 
            f"UUID {uuid_str} already exists. Use PUT /update/{uuid_str} to append data."
        )

    raw_name = post_request.file_name or f"{uuid_str}_{post_request.date}.pdf"
    final_file_name = sanitize_filename(raw_name)
    file_path = os.path.join(UPLOAD_DIR, final_file_name)
    
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        extracted_text = extract_text_from_pdf(file_path)
        if extracted_text is None:
            raise HTTPException(500, "Failed to extract text from PDF.")

        data_store[uuid_str] = {
            "file_name": final_file_name,
            "date": post_request.date,
            "text": extracted_text
        }

        return {
            "message": "File uploaded and text extracted successfully.",
            "uuid": uuid_str,
            "file_name": final_file_name,
            "date": post_request.date
        }

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


# ----------------------------
# 3) Update Existing PDF (JWT Protected)
# ----------------------------
@router.put("/update/{uuid}")
async def update_pdf_data(
    uuid: uuid.UUID,
    file: UploadFile = File(...),
    file_name: Optional[str] = Form(None),
    date: Optional[str] = Form(None),
    current_user: dict = Depends(get_current_user)
):
    """
    Append new PDF text to existing UUID data.
    Requires JWT authentication via Bearer token.
    """
    post_request = PostRequest(
        file_name=file_name,
        date=date
    )

    uuid_str = str(uuid)

    if file.content_type != "application/pdf":
        raise HTTPException(400, "Invalid file type. Only PDF files are accepted.")

    if uuid_str not in data_store:
        raise HTTPException(404, f"UUID {uuid_str} not found. Upload first.")
    
    raw_name = post_request.file_name or f"{uuid_str}_{post_request.date}.pdf"
    final_file_name = sanitize_filename(raw_name)
    file_path = os.path.join(UPLOAD_DIR, final_file_name)

    try:
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        new_text = extract_text_from_pdf(file_path)
        if new_text is None:
            raise HTTPException(500, "Failed to extract text from PDF.")

        data_store[uuid_str]["text"] += "\n\n" + new_text

        return {
            "message": "New PDF text appended successfully.",
            "uuid": uuid_str,
            "file_name": final_file_name,
            "date": post_request.date
        }

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


# ----------------------------
# 4) Query Stored Text (JWT Protected)
# ----------------------------
@router.get("/query/{uuid}")
async def query_data(
    uuid: uuid.UUID,
    query: str = Query(..., description="The question you want to ask"),
    current_user: dict = Depends(get_current_user)
):
    """
    Query the stored PDF text using LLM.
    Requires JWT authentication via Bearer token.
    """
    uuid_str = str(uuid)
    
    if uuid_str not in data_store:
        raise HTTPException(404, f"UUID {uuid_str} not found.")

    stored = data_store[uuid_str]
    llm_response = get_llm_response(context=stored["text"], query=query)

    return {
        "uuid": uuid_str,
        "file_name": stored["file_name"],
        "date": stored["date"],
        "query": query,
        "llm_response": llm_response
    }


# ----------------------------
# 5) Delete Data (JWT Protected)
# ----------------------------
@router.delete("/delete/{uuid}")
async def delete_data(
    uuid: uuid.UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete stored data for a UUID.
    Requires JWT authentication via Bearer token.
    """
    uuid_str = str(uuid)
    
    if uuid_str not in data_store:
        raise HTTPException(404, f"UUID {uuid_str} not found.")

    deleted = data_store.pop(uuid_str)
    
    return {
        "message": f"Data for UUID {uuid_str} deleted successfully.",
        "file_name": deleted["file_name"],
        "date": deleted["date"]
    }


# ----------------------------
# 6) List All UUIDs (JWT Protected)
# ----------------------------
@router.get("/list_uuids")
async def list_all_uuids(current_user: dict = Depends(get_current_user)):
    """
    List all stored UUIDs with their metadata.
    Requires JWT authentication via Bearer token.
    """
    result = []
    for uuid_key, data in data_store.items():
        result.append({
            "uuid": uuid_key,
            "file_name": data["file_name"],
            "date": data["date"]
        })
    
    return {"items": result}