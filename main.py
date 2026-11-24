from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_db
from routers import auth, ai

app = FastAPI(title="Modular FastAPI + Auth + SQLite + Gemini AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db()

app.include_router(auth.router)
app.include_router(ai.router)

@app.get("/")
def root():
    return {"status": "live"}
