from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Local imports
from ingest import load_text, chunk_text
from vector_store import save_to_faiss
from rag import ask_question

# App init
app = FastAPI(title="AI-Powered HR Onboarding Assistant")

# CORS (keep open for now)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directories
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ------------------------
# Health Check
# ------------------------
@app.get("/")
def health():
    return {"status": "ok"}

# ------------------------
# Admin: Upload HR Docs
# ------------------------
@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Ingest
    text = load_text(file_path)
    chunks = chunk_text(text)

    metadata = [{"source": file.filename} for _ in chunks]

    save_to_faiss(chunks, metadata)

    return {
        "message": "Document uploaded and indexed successfully",
        "chunks_created": len(chunks),
        "document": file.filename
    }

# ------------------------
# User: Ask Questions
# ------------------------
class Question(BaseModel):
    question: str

@app.post("/ask")
def ask(q: Question):
    answer, sources = ask_question(q.question)

    return {
        "question": q.question,
        "answer": answer,
        "sources": sources
    }
