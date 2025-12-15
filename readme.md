# 🚀 CAG Project API - Chat with Your PDF
Welcome to the CAG Project API, a simple yet powerful system to manage and interact with PDF documents using AI. This guide will help new users understand, set up, and use the project from A to Z.

# 📌 Project Overview
The CAG Project API allows users to:

- Upload and store PDF files
- Extract and query text from PDFs
- Update existing PDFs with new content
- Delete stored PDFs
- Interact with stored data using a Large Language Model (LLM)
- Authenticate users and protect API endpoints with JWT

This project is designed for learning, testing, and building AI-driven document systems.

# 📂 CAG Project - Complete Structure
CAG Project Code/
│
├── main.py                     # Entry point of the FastAPI application
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (API keys, JWT secret)
│
├── src/
│   ├── routers/
│   │   ├── data_handler.py     # Handles PDF CRUD, querying, JWT verification
│   │   │                       # ✅ Added filename sanitization
│   │   ├── user_auth.py        # Signup and Login endpoints
│   │   │
│   │   └── models/
│   │       ├── post_request.py # Pydantic model for PDF uploads/updates
│   │       └── user_models.py  # Pydantic models for user signup/login
│   │
│   ├── services/
│   │   ├── user_service.py     # User creation & authentication logic
│   │   └── jwt_service.py      # JWT token creation and verification
│   │
│   ├── utils/
│   │   ├── pdf_processor.py    # PDF text extraction
│   │   ├── llm_client.py       # Interact with LLM (AI) for queries
│   │   ├── password_utils.py   # Password hashing and verification
│   │   ├── uuid_utils.py       # Generate UUIDs
│   │   └── filename_sanitizer.py  # ✅ Filename sanitization utility
│   │
│   ├── data_store.py           # Temporary storage for PDF uploads and extracted text
│   │
│   └── database/
│       └── memory_db.py        # Temporary user database (signup/authentication)
│
└── README.md                   # Project documentation



# ⚙️ Features & Functionality

## 1. User Authentication (JWT)
- Users can signup and login.
- Passwords are hashed securely.
- Login provides a JWT token used to access protected endpoints.
- JWT token ensures secure operations on PDF files.

## 2. UUID Mechanism
- Each PDF upload is linked with a unique UUID.
- Users can generate a UUID before uploading files (`/take_uuid` endpoint).
- UUID helps track and manage files easily.

## 3. PDF Management
All PDF operations are JWT-protected:

- **Upload PDF (POST /upload/{uuid})**  
  - Upload a new PDF.  
  - Extract text automatically.  
  - Store metadata and extracted text in memory.

- **Update PDF (PUT /update/{uuid})**  
  - Append new content from another PDF to an existing UUID.

- **Query PDF (GET /query/{uuid})**  
  - Ask questions to AI based on PDF text.  
  - Returns AI-generated responses using LLM.

- **Delete PDF (DELETE /data/{uuid})**  
  - Remove PDF and its text from memory.

- **List All UUIDs (GET /list_uuids)**  
  - View all uploaded UUIDs with associated metadata.

# 🧰 Utilities
- **Password Utils**: Secure hashing and verification.
- **PDF Processor**: Extract text from PDF files.
- **LLM Client**: Send queries to AI and receive answers.
- **UUID Utils**: Generate unique IDs for files.

# ⚡ Setup & Run
Clone the repository:

```bash
git clone <repository-url>
cd "CAG Project Code"

Create Conda environment and install dependencies:

conda create -n python-project python=3.11 -y
conda activate python-project
pip install -r requirements.txt


Add environment variables in .env:

GEMINI_API_KEY=<Your Google Gemini API Key>


Run the FastAPI application:

python main.py


Access the API docs:

Swagger UI: http://127.0.0.1:8001/docs

ReDoc: http://127.0.0.1:8001/redoc

# 🔐 Security Notes

JWT tokens protect critical endpoints.

Always keep your API keys and .env secure.

Passwords are hashed before storing in memory.

🎯 Quick Start Example

Signup a new user:

POST /api/v1/signup
{
    "name": "Alice",
    "email": "alice@example.com",
    "password": "secure123",
    "country": "Pakistan"
}


Login to get JWT:

POST /api/v1/login
{
    "email": "alice@example.com",
    "password": "secure123"
}


Upload PDF using JWT:

POST /api/v1/upload/<UUID>
Headers: Authorization: Bearer <JWT>


Query PDF:

GET /api/v1/query/<UUID>?query=What is in the document?
Headers: Authorization: Bearer <JWT>

# ✅ Summary

Complete PDF management system

AI-driven query support

User authentication and JWT verification

Temporary in-memory storage

Easy-to-understand, beginner-friendly structure