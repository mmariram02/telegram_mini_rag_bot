import os
import sqlite3
import glob
import numpy as np
from sentence_transformers import SentenceTransformer

DATA_DIR = "data"
DB_PATH = "rag_vectors.db"
MODEL_NAME = "all-MiniLM-L6-v2"

def load_documents():
    docs = []
    pattern = os.path.join(DATA_DIR, "*.*")
    for path in glob.glob(pattern):
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            docs.append((os.path.basename(path), text))
    return docs

def chunk_text(text, max_chars=500):
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    chunks = []
    current = ""
    for p in paragraphs:
        if len(current) + len(p) + 1 <= max_chars:
            current += (" " if current else "") + p
        else:
            if current:
                chunks.append(current)
            current = p
    if current:
        chunks.append(current)
    return chunks

def init_db(conn):
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_name TEXT,
            text TEXT,
            embedding BLOB
        )
        """
    )
    conn.commit()

def main():
    print("📂 Loading documents from:", DATA_DIR)
    docs = load_documents()
    if not docs:
        print("❗ No documents found. Please add text/markdown files into the 'data' folder.")
        return

    print(f"✅ Found {len(docs)} documents.")
    model = SentenceTransformer(MODEL_NAME)

    conn = sqlite3.connect(DB_PATH)
    init_db(conn)
    cur = conn.cursor()

    for doc_name, text in docs:
        chunks = chunk_text(text)
        print(f"📄 {doc_name}: {len(chunks)} chunks")
        embeddings = model.encode(chunks)
        for chunk_text_value, emb in zip(chunks, embeddings):
            emb_bytes = np.asarray(emb, dtype=np.float32).tobytes()
            cur.execute(
                "INSERT INTO chunks (doc_name, text, embedding) VALUES (?, ?, ?)",
                (doc_name, chunk_text_value, emb_bytes),
            )

    conn.commit()
    conn.close()
    print("✅ RAG SQLite database built at:", DB_PATH)

if __name__ == "__main__":
    main()
