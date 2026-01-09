import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Load env even if imported independently
load_dotenv()

VECTOR_PATH = "vector_store"

def get_embeddings():
    return OpenAIEmbeddings()

def save_to_faiss(chunks, metadatas, path=VECTOR_PATH):
    os.makedirs(path, exist_ok=True)

    embeddings = get_embeddings()
    index_path = os.path.join(path, "index.faiss")

    if os.path.exists(index_path):
        db = FAISS.load_local(
            path,
            embeddings,
            allow_dangerous_deserialization=True
        )
        db.add_texts(texts=chunks, metadatas=metadatas)
    else:
        db = FAISS.from_texts(
            texts=chunks,
            embedding=embeddings,
            metadatas=metadatas
        )

    db.save_local(path)
    return db
