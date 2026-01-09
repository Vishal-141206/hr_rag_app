import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

VECTOR_PATH = "vector_store"

from langchain_community.embeddings import HuggingFaceEmbeddings

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

def get_llm():
    return ChatOpenAI(model="gpt-4o-mini", temperature=0)

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

    docs = db.similarity_search(question, k=3)

    if not docs:
        return "I don't know based on the provided documents.", []

    context_blocks = []
    sources = set()

    for d in docs:
        src = d.metadata.get("source", "Unknown")
        sources.add(src)
        context_blocks.append(f"[Source: {src}]\n{d.page_content}")

    context = "\n\n".join(context_blocks)

    prompt = f"""
You are an HR onboarding assistant.

Rules:
- Use ONLY the context below.
- Do NOT use prior knowledge.
- If answer is missing, say:
  "I don't know based on the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""

    llm = get_llm()
    response = llm.invoke(prompt)

    return response.content.strip(), list(sources)
