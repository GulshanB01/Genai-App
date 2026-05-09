#  Smart Notes GenAI Assistant

Smart Notes AI Assistant is an intelligent document-based Q&A system that allows users to upload their notes (PDF or text files) and ask questions directly from them.  
The system performs text extraction, chunking, BM25 semantic retrieval, and answer generation using the **Groq API (LLaMA 3.3 70B)**.

The backend is powered by **FastAPI**, with support for document upload, question answering, and feedback logging for future model fine-tuning.

---

##  Live Demo

 **Try the app here:**  
[https://genai-app-production-267e.up.railway.app/docs](https://genai-app-production-267e.up.railway.app/docs)

---

##  Features

###  1. Document Upload

Supports the following formats:

* **PDF**
* **TXT**
* **MD**

---

###  2. Intelligent Text Chunking & Retrieval

* The system breaks long documents into smaller chunks.
* Uses **BM25Okapi** to retrieve the most relevant chunks from notes.
* Ensures highly accurate, context-grounded question answering.

---

###  3. LLaMA-Powered Question Answering

* Uses **LLaMA 3.3 70B** via the **Groq API** for fast, high-quality answers.
* Model answers **only from the retrieved user notes**.
* If the answer is not found, the system explicitly says so.

---

###  4. User Authentication

* Login & Signup system
* Every user has dedicated storage & credits
* Passwords stored in a JSON database

---

###  5. Credit System

* Each user starts with default credits
* 1 credit = 1 question answered
* Manual credit addition UI included

---

###  6. Feedback Logging

All feedback is stored in:

```
data/user_feedback.jsonl
```

This can later be used for model evaluation or fine-tuning.

---

##  Application Workflow

1. User logs in / signs up
2. Uploads documents (PDF / TXT / MD)
3. Text is extracted & chunked
4. BM25 retrieves the most relevant chunks
5. Chunks + question → sent to Groq (LLaMA 3.3 70B)
6. Answer generated
7. Credit deducted
8. User can submit feedback

---

##  Project Structure

```
├── main.py                    # FastAPI backend
├── requirements.txt           # Python dependencies
├── data/
│   ├── users.json             # User database
│   ├── user_feedback.jsonl    # Feedback logs
│   └── uploaded/              # User-uploaded files
```

---

## 🛠️ Technologies Used

### Backend / AI

* Python
* FastAPI + Uvicorn
* Groq API (LLaMA 3.3 70B)

### Document Processing

* PyPDF2
* BM25 (rank_bm25)
* NumPy

---

##  Local Installation

### 1️ Clone the repository

```bash
git clone https://github.com/<your-username>/<repo-name>
cd <repo-name>
```

### 2️ Create & activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate     # Mac/Linux
.venv\Scripts\activate        # Windows
```

### 3️ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️ Set your Groq API key

Create a `.env` file or export the variable:

```bash
export GROQ_API_KEY=your_groq_api_key_here
```

### 5️ Run the backend

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

---

## 📡 API Endpoints

| Method | Endpoint    | Description                        |
|--------|-------------|------------------------------------|
| GET    | `/`         | Health check                       |
| POST   | `/upload`   | Upload a PDF, TXT, or MD file      |
| POST   | `/ask`      | Ask a question from uploaded notes |
| POST   | `/feedback` | Submit feedback on an answer       |

---

## 📝 API Usage Examples

### Upload a document

```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@my_notes.pdf"
```

### Ask a question

```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the water cycle?", "top_k": 5}'
```

### Submit feedback

```bash
curl -X POST "http://localhost:8000/feedback" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the water cycle?",
    "answer": "The water cycle is...",
    "helpful": "yes",
    "user_correct_answer": ""
  }'
```

---

## Deployment

This FastAPI backend can be deployed on any platform that supports Python:

* **Railway** / **Render** — push repo and set `GROQ_API_KEY` as an environment variable
* **Heroku** — use the included `Procfile`
* **Docker** — containerize with a standard Python Dockerfile

---

##  Summary

Smart Notes AI Assistant transforms static documents into an interactive question-answering experience.  
Ideal for students, professionals, and educators who want fast, accurate answers grounded in their own notes.

---
