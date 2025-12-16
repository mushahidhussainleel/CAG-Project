# 🚀 CAG Project (Backend)

**Chat with Your PDFs using AI – FastAPI Backend**
[![CAG Project Preview](https://claude.ai/public/artifacts/42649292-6467-4ace-b3b5-3b6736b40c17)](https://claude.ai/public/artifacts/42649292-6467-4ace-b3b5-3b6736b40c17)


A clean, secure, and extensible **backend-only FastAPI project** that allows users to upload PDF documents, extract text, and query them using AI (Google Gemini). This project is designed as a **learning-focused backend portfolio project**, suitable for internships, resume showcasing, and as a foundation for future ML/AI systems.

---

## 📌 Project Purpose

The **CAG Project** is intentionally built as a **backend-first system**:

* 🎯 Strengthen Python & FastAPI skills
* 🎯 Practice authentication, API design, and clean architecture
* 🎯 Build a solid base for future **ML / AI integrations**
* 🎯 Showcase real-world backend practices for internships

> ❗ This repository does **not** include any frontend/UI.
> APIs are tested and explored via **Swagger UI**.

---

## ✨ Key Features

### 🔐 Authentication & Security

* User signup & login
* Password hashing using **bcrypt**
* JWT-based authentication
* Protected API routes

### 📄 PDF Handling

* Upload PDF files
* Automatic text extraction
* Query PDFs using natural language
* Update (append-style) PDF content
* Delete stored PDFs
* List all stored document UUIDs

### 🤖 AI Integration

* Google Gemini API for document-based Q&A
* Context-aware responses from extracted PDF text

### 🧱 Clean Architecture

* Modular folder structure
* Clear separation of concerns (routers, services, utils)
* Easy to extend (DB, vector search, embeddings, ML models)

---

## 🏗️ Tech Stack

* **Language**: Python 3.11
* **Framework**: FastAPI
* **Authentication**: JWT (JSON Web Tokens)
* **AI**: Google Gemini API
* **PDF Processing**: PyPDF2
* **Storage**: In-memory (for learning & simplicity)

---

## 📂 Project Structure

```
CAG-Project/
│
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variable template
├── .gitignore                 # Git ignore rules
├── README.md                  # Project documentation
│
└── src/
    ├── routers/               # API route definitions
    │   ├── data_handler.py    # PDF CRUD & query APIs
    │   ├── user_auth.py       # Authentication APIs
    │   └── models/            # Pydantic request/response models
    │
    ├── services/              # Business logic
    │   ├── user_service.py
    │   └── jwt_service.py
    │
    ├── utils/                 # Helper utilities
    │   ├── pdf_processor.py
    │   ├── llm_client.py
    │   ├── password_utils.py
    │   ├── uuid_utils.py
    │   └── filename_sanitizer.py
    │
    ├── data_store.py          # In-memory document storage
    └── database/
        └── memory_db.py       # In-memory user storage
```

---

## 🚀 Getting Started

### Prerequisites

* Python 3.11+
* Conda (recommended) or pip
* Google Gemini API Key

### Installation

```bash
git clone https://github.com/mushahidhussainleel/CAG-Project.git
cd CAG-Project
```

```bash
conda create -n cag-project python=3.11 -y
conda activate cag-project
```

```bash
pip install -r requirements.txt
```

---

## 🔧 Environment Configuration

Create a `.env` file using the example:

```bash
cp .env.example .env
```

Add your API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
HOST=127.0.0.1
PORT=8001
```

> ⚠️ `.env` is intentionally ignored by Git.

---

## ▶️ Running the Application

```bash
python main.py
```

Access the API docs:

* Swagger UI: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)
* ReDoc: [http://127.0.0.1:8001/redoc](http://127.0.0.1:8001/redoc)

---

## 📡 API Overview

### Authentication

| Method | Endpoint         | Description         |
| ------ | ---------------- | ------------------- |
| POST   | `/api/v1/signup` | Register new user   |
| POST   | `/api/v1/login`  | Login & receive JWT |

### PDF Operations (JWT Required)

| Method | Endpoint                | Description            |
| ------ | ----------------------- | ---------------------- |
| GET    | `/take_uuid`            | Generate document UUID |
| POST   | `/api/v1/upload/{uuid}` | Upload PDF             |
| GET    | `/api/v1/query/{uuid}`  | Query PDF with AI      |
| PUT    | `/api/v1/update/{uuid}` | Update PDF content     |
| DELETE | `/api/v1/data/{uuid}`   | Delete PDF             |
| GET    | `/api/v1/list_uuids`    | List all documents     |

---

## 🎯 Learning Outcomes

This project demonstrates:

* REST API design with FastAPI
* Authentication & authorization flows
* Secure password handling
* Clean backend architecture
* Practical AI API integration
* Backend preparation for ML systems

---

## 🔮 Future Enhancements (Optional)

* Persistent database (PostgreSQL / MongoDB)
* Vector embeddings & semantic search
* File-based or cloud storage
* Rate limiting & logging
* ML-based document summarization

---

## 👨‍💻 Author

**Mushahid Hussain Leel**

* GitHub: [https://github.com/mushahidhussainleel](https://github.com/mushahidhussainleel)
* Repository: [https://github.com/mushahidhussainleel/CAG-Project](https://github.com/mushahidhussainleel/CAG-Project)

---

## ⭐ Support

If this project helped you:

* ⭐ Star the repository
* 🐞 Open issues for improvements
* 📚 Use it as a learning reference

---

**This project is intentionally backend-only and focused on learning, clarity, and future ML growth.**
