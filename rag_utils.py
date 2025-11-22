import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import os

# Initialize embedding model (local)
_EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
_embed_model = SentenceTransformer(_EMBED_MODEL_NAME)

# Initialize OpenAI client (for generation)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "ADD_YOUR_OPENAI_KEY_HERE")
_client = OpenAI(api_key=OPENAI_API_KEY)

DB_PATH = "rag_vectors.db"

def _get_connection():
    return sqlite3.connect(DB_PATH)

def _cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    if a.ndim > 1:
        a = a[0]
    if b.ndim > 1:
        b = b[0]
    denom = (np.linalg.norm(a) * np.linalg.norm(b)) + 1e-10
    return float(np.dot(a, b) / denom)

def _retrieve_top_k(query_embedding, k=3):
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, doc_name, text, embedding FROM chunks")
    rows = cursor.fetchall()
    conn.close()

    scored = []
    for _id, doc_name, text, emb_blob in rows:
        emb = np.frombuffer(emb_blob, dtype=np.float32)
        score = _cosine_similarity(query_embedding, emb)
        scored.append((score, doc_name, text))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:k]

def answer_query(query: str) -> str:
    # Main RAG pipeline:
    # 1. Embed query
    # 2. Retrieve top-k chunks from SQLite
    # 3. Build context
    # 4. Call LLM (or return context if no key)
    if not query.strip():
        return "Please provide a non-empty query."

    # Step 1: Embed query
    q_emb = _embed_model.encode([query])[0]

    # Step 2: Retrieve top-k chunks
    top_chunks = _retrieve_top_k(q_emb, k=3)
    if not top_chunks:
        return "No knowledge base found. Please run build_db.py first."

    context_parts = []
    for score, doc_name, text in top_chunks:
        context_parts.append(f"[{doc_name}] {text}")

    context = "\n\n".join(context_parts)

    # If no real API key, just return context
    if OPENAI_API_KEY.startswith("ADD_YOUR_OPENAI_KEY"):
        return (
            "🔎 Top matching context snippets (no LLM key set):\n\n"
            + context
        )

    prompt = (
        "You are a helpful assistant answering based only on the provided context.\n"
        "If the answer is not in the context, say you don't know.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n\n"
        "Answer in 3–5 sentences:\n"
    )

    completion = _client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=300,
    )

    answer = completion.choices[0].message.content.strip()
    # Append sources
    sources = "\n".join({f"- {doc_name}" for _, doc_name, _ in top_chunks})
    answer += "\n\nSources:\n" + sources
    return answer
