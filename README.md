#  Smart Notes GenAI Assistant

Smart Notes AI Assistant is an intelligent document-based Q&A system that allows users to upload their notes (PDF or text files) and ask questions directly from them.
The system performs text extraction, chunking, semantic retrieval, and answer generation using a T5 model.

The web app is deployed on **Streamlit Cloud**, with support for authentication, credit usage, and feedback logging for future model fine-tuning.

---

##  Live Demo

🔗 **Try the app here:**
https://genai-app-production-267e.up.railway.app/docs

---

##  Features

###  1. Document Upload

Supports the following formats:

* **PDF**
* **TXT**
* **MD**

( *Image OCR removed from this version to improve stability on Streamlit Cloud.*)

---

###  2. Intelligent Text Chunking & Retrieval

* The system breaks long documents into smaller chunks.
* Uses **BM25Okapi** to retrieve the most relevant chunks from notes.
* Ensures highly accurate question answering.

---

###  3. T5 Question Answering

* Uses a **fine-tuned or base T5 model** for generating answers.
* Model answers **only from the retrieved user notes**.
* If the answer is not found, the system explicitly says so.

---

###  4. User Authentication

* Login & Signup system
* Every user has dedicated storage & credits
* Passwords stored in JSON database

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

This can later be used to fine-tune the T5 model for better accuracy.

---

##  Application Workflow

1. User logs in / signs up
2. Uploads documents (PDF/TXT/MD)
3. Text is extracted & chunked
4. BM25 retrieves relevant chunks
5. Chunks + question → sent to T5 model
6. Answer generated
7. Credit deducted
8. User can submit feedback

---

##  Project Structure

```
├── app.py                     # Main Streamlit application
├── finetune_t5.py             # Script for optional T5 fine-tuning
├── requirements.txt           # Python dependencies
├── data/
│   ├── users.json             # User database
│   ├── user_feedback.jsonl    # Feedback logs
│   └── uploaded/              # User-uploaded files
├── models/
│   └── finetuned_t5/          # Optional fine-tuned model
```

---

##  Technologies Used

###  Backend / ML

* Python
* HuggingFace Transformers
* T5 (base or fine-tuned)
* TensorFlow 

###  Document Processing

* PyPDF2
* BM25 (rank_bm25)
* PIL

###  Frontend

* Streamlit
* Custom authentication & credit system

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

### 4️ Run the app

```bash
streamlit run app.py
```

---

##  Deployment (Streamlit Cloud)

1. Push the repo to GitHub
2. Visit: [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Create new app
4. Select repo
5. Choose `app.py` as entry file
6. Deploy 

Streamlit Cloud automatically installs `requirements.txt`.

---

##  Fine-Tuning the T5 Model (Optional)

1. Collect user feedback in `data/user_feedback.jsonl`
2. Train using:

```bash
python finetune_t5.py
```

3. Save the trained model to:

```
models/finetuned_t5/
```

4. Update model path inside `app.py`:

```python
MODEL_NAME = "models/finetuned_t5"
```

---

##  Summary

Smart Notes AI Assistant transforms static documents into an interactive question-answering experience.
Ideal for students, professionals, and educators who want fast, accurate answers based on their own notes.

---
