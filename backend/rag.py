import os
import numpy as np
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

VECTOR_PATH = "vector_store"

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def ask_question(question: str):
    index_path = os.path.join(VECTOR_PATH, "index.faiss")

    if not os.path.exists(index_path):
        return "No HR documents have been uploaded yet.", []

    embeddings = get_embeddings()

    db = FAISS.load_local(
        VECTOR_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    docs = db.similarity_search(question, k=4)

    if not docs:
        return "I don't know based on the provided documents.", []

    # ---- Sentence-level ranking ----
    sentences = []
    sources = set()

    for d in docs:
        src = d.metadata.get("source", "Unknown document")
        sources.add(src)
        for s in d.page_content.split("."):
            s = s.strip()
            if len(s) > 20:
                sentences.append((s, src))

    if not sentences:
        return "I don't know based on the provided documents.", list(sources)

    q_emb = embeddings.embed_query(question)

    scored = []
    for sent, src in sentences:
        s_emb = embeddings.embed_query(sent)
        score = cosine_sim(q_emb, s_emb)
        scored.append((score, sent, src))

    scored.sort(reverse=True, key=lambda x: x[0])

    # Take top 3 best sentences
    best_sentences = [s for _, s, _ in scored[:3]]

    answer = ". ".join(best_sentences)
    if not answer.endswith("."):
        answer += "."

    return answer, list(sources)
