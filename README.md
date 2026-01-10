# AI-Powered HR Onboarding Assistant

## Overview
This project implements a Retrieval-Augmented Generation (RAG) system that allows HR teams
to upload internal policy documents and enables employees to query them using natural language.
The assistant provides accurate, document-grounded answers with clear citations.

## Features
- Upload HR documents (PDF, DOCX, TXT)
- Semantic search using FAISS vector database
- Context-aware answers with zero hallucination
- Automatic query categorization (Benefits, Legal, Culture)
- Source citations for transparency
- Admin dashboard to view and delete documents
- Clean and intuitive frontend interface

## Architecture
1. Document ingestion and text extraction
2. Intelligent chunking using recursive character splitting
3. Vector embedding using SentenceTransformers
4. FAISS similarity search for retrieval
5. Extractive answer generation with sentence ranking

## Tech Stack
- Backend: FastAPI
- Frontend: React + Vite
- Vector DB: FAISS
- Embeddings: all-MiniLM-L6-v2 (HuggingFace)
- Language: Python, JavaScript

## Setup Instructions

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --reload
