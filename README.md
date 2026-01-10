# AI-Powered HR Onboarding Assistant

## 1. Background

HR teams spend significant time answering repetitive questions from new hires related to company policies, benefits, and administrative procedures.  
To scale the onboarding process, this project implements a **Self-Service Knowledge Assistant** that allows employees to query internal HR documents using natural language.

---

## 2. Problem Statement

Build a **Retrieval-Augmented Generation (RAG)** application that:
- Allows HR admins to upload policy documents
- Enables employees to ask questions in natural language
- Provides accurate, context-aware answers
- Avoids hallucinations
- Includes clear citations from source documents

---

## 3. Features

### Employee Features
- Ask natural language questions about HR policies
- Receive accurate answers strictly based on uploaded documents
- View source document citations
- Automatic query categorization (Benefits, Legal, Internal Culture, General)

### Admin Features
- Upload HR policy documents (PDF, DOCX, TXT)
- View all uploaded documents
- Delete documents from the knowledge base

---

## 4. System Architecture

The system follows a modular **Retrieval-Augmented Generation (RAG)** pipeline:

1. **Document Ingestion**
   - Supports PDF, DOCX, and TXT files
   - Extracts raw text
   - Applies intelligent chunking with overlap

2. **Embedding & Vector Storage**
   - Uses HuggingFace SentenceTransformers (`all-MiniLM-L6-v2`)
   - Stores embeddings in FAISS for efficient similarity search

3. **Retrieval**
   - Performs semantic similarity search over document chunks
   - Ranks content based on relevance to the user query

4. **Answer Generation**
   - Uses extractive, sentence-level answering
   - Answers are strictly derived from retrieved document content
   - No hallucinations by design

5. **API Layer**
   - FastAPI backend handling uploads, queries, and admin actions

6. **Frontend**
   - React + Vite interface for employees and admins

---

## 5. Tech Stack

- **Backend:** FastAPI (Python)
- **Frontend:** React + Vite
- **Vector Database:** FAISS
- **Embeddings:** HuggingFace SentenceTransformers
- **Languages:** Python, JavaScript

---

## 6. Setup Instructions

### Prerequisites
- Python **3.10+**
- Node.js **v18+**
- npm
- Git

---

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --reload

---

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
