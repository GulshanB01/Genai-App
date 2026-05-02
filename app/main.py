from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from pathlib import Path
from io import BytesIO
from PyPDF2 import PdfReader
import numpy as np
from rank_bm25 import BM25Okapi
import json, os

app = FastAPI(title="Smart Notes AI Backend")

DATA_DIR = Path("data")
UPLOAD_DIR = DATA_DIR / "uploaded"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# In-memory storage
docs = []
bm25 = None
# Load T5 model once at startup

from groq import Groq
groq_client = Groq(api_key="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")
# ---------------- HELPERS ----------------

def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes))
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def chunk_text(text: str, max_chars: int = 1000) -> list:
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    chunks, current = [], ""
    for p in paragraphs:
        if len(current) + len(p) + 1 <= max_chars:
            current += " " + p
        else:
            if current:
                chunks.append(current.strip())
            current = p
    if current:
        chunks.append(current.strip())
    return chunks

def build_bm25():
    global bm25
    if docs:
        bm25 = BM25Okapi([d.split() for d in docs])

def retrieve_chunks(query: str, top_k: int = 5):
    if bm25 is None or not docs:
        return []
    scores = np.array(bm25.get_scores(query.split()))
    top_idxs = scores.argsort()[-top_k:][::-1]
    return [(docs[i], float(scores[i])) for i in top_idxs]

# ---------------- ROUTES ----------------

@app.get("/")
def root():
    return {"message": "Smart Notes API is running!"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_bytes = await file.read()
    ext = file.filename.lower().split(".")[-1]

    if ext == "pdf":
        text = extract_text_from_pdf(file_bytes)
    elif ext in ["txt", "md"]:
        text = file_bytes.decode("utf-8", errors="ignore")
    else:
        return {"error": "Unsupported file type. Use PDF, TXT, or MD."}

    chunks = chunk_text(text)
    docs.extend(chunks)
    build_bm25()

    return {
        "filename": file.filename,
        "chunks_added": len(chunks),
        "total_chunks": len(docs)
    }

class AskRequest(BaseModel):
    question: str
    top_k: int = 5

@app.post("/ask")
def ask_question(req: AskRequest):
    if not docs:
        return {"error": "No documents uploaded yet."}

    retrieved = retrieve_chunks(req.question, req.top_k)
    if not retrieved:
        return {"error": "No relevant chunks found."}

    context = "\n\n".join([chunk for chunk, score in retrieved])
    if len(context) > 3000:
        context = context[:3000]

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful study assistant. Use ONLY the given context to answer. If the answer is not in the context, say: I couldn't find this in the notes."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {req.question}"
            }
        ],
        max_tokens=512
    )

    answer = response.choices[0].message.content.strip()

    return {
        "question": req.question,
        "answer": answer,
        "chunks_found": len(retrieved)
    }

FEEDBACK_PATH = DATA_DIR / "user_feedback.jsonl"

class FeedbackRequest(BaseModel):
    question: str
    answer: str
    helpful: str
    user_correct_answer: str = ""

@app.post("/feedback")
def submit_feedback(req: FeedbackRequest):
    entry = {
        "question": req.question,
        "answer": req.answer,
        "helpful": req.helpful,
        "user_correct_answer": req.user_correct_answer,
    }
    with open(FEEDBACK_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    return {"message": "Feedback saved!"}