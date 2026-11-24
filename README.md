# fastapi-gemini-ai-backend
Modular FastAPI backend featuring OAuth2/JWT authentication, SQLModel (SQLite) CRUD persistence, and Google Gemini AI integration with multi-model fallback.
# Modular FastAPI + JWT Auth + SQLite + Gemini AI Backend

A clean, modular REST API built with **FastAPI**, **SQLModel (SQLite)**, **OAuth2 / JWT Authentication**, and the **Google Gemini API** (with multi-model fallback).

## Features
- **Modular Architecture:** Separated into routers, services, database engine, models, and Pydantic schemas.
- **Authentication & Security:** Password hashing with Argon2 (`pwdlib`) and stateless JWT Bearer token authentication (`PyJWT`), with per-user data isolation.
- **Persistent CRUD History:** Full Create, Read, Update, and Delete operations for AI prompt history stored in SQLite via `SQLModel`.
- **Resilient Gemini AI Integration:** Automatic fallback across multiple Gemini Flash models (`gemini-2.5-flash-lite`, `gemini-3.5-flash`, `gemini-3.8-flash`) with graceful offline fallback handling.

## Project Structure
```text
FastAPI/
├── main.py                  # FastAPI entry point & router registration
├── database.py              # SQLite database engine & session dependency
├── models.py                # SQLModel database tables (User, AIHistory)
├── schemas.py               # Pydantic request/response schemas
├── routers/
│   ├── auth.py              # /auth/signup & /auth/login endpoints
│   └── ai.py                # Protected /ai/ask & /ai/history CRUD endpoints
├── services/
│   └── ai_service.py        # Google Gemini SDK client & model fallback logic
├── requirements.txt         # Python dependencies
└── .gitignore               # Excludes .env, *.db, venv/, and __pycache__/
```

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com
   cd fastapi-gemini-ai-backend
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   # source venv/bin/activate # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_google_ai_studio_api_key
   SECRET_KEY=your_random_hex_secret_key
   ```

5. **Run the server**
   ```bash
   fastapi dev main.py
   ```
   Open interactive Swagger docs at **`http://127.0.0`**.

## API Endpoints

| Method | Endpoint | Auth Required | Description |
| :--- | :--- | :---: | :--- |
| `POST` | `/auth/signup` | No | Register a new user account |
| `POST` | `/auth/login` | No | Authenticate and receive a JWT Bearer token |
| `POST` | `/ai/ask` | Yes | Send a prompt to Gemini AI and save the response |
| `GET` | `/ai/history` | Yes | Retrieve all saved AI prompts for the logged-in user |
| `PUT` | `/ai/history/{record_id}` | Yes | Update a prompt and regenerate its AI response |
| `DELETE` | `/ai/history/{record_id}` | Yes | Delete a specific saved AI record |
