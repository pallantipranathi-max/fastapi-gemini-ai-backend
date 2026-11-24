from fastapi import FastAPI
from database import create_db
from routers import auth, ai

app = FastAPI(title="Modular FastAPI + Auth + SQLite + Gemini AI")

@app.on_event("startup")
def on_startup():
    create_db()

app.include_router(auth.router)
app.include_router(ai.router)

@app.get("/")
def root():
    return {"status": "live"}
