# 🧠 Mini-RAG Telegram Bot (Option A — Text RAG)

This project implements the **Mini-RAG Telegram Bot** variant described in the assignment.

The bot can:
- Receive user questions via Telegram
- Retrieve relevant chunks from a small local knowledge base
- Use a small LLM (OpenAI GPT-3.5) to generate a summarized answer
- Return the answer along with source document names

## 📁 Project Structure

```bash
telegram_mini_rag_bot/
├── app.py               # Telegram bot entry point
├── rag_utils.py         # RAG pipeline: retrieval + generation
├── build_db.py          # Script to build SQLite vector store
├── requirements.txt     # Python dependencies
├── README.md            # This file: setup + explanation
├── rag_vectors.db       # (created after running build_db.py)
├── data/                # 3–5 sample documents for RAG
├── diagrams/
│   └── architecture.md  # System design diagram (text-based)
└── screenshots/
    └── README.txt       # Instructions for adding demo screenshots
```

## ⚙ Tech Stack (as per assignment)

- Bot framework: `python-telegram-bot`
- Embeddings model: `sentence-transformers/all-MiniLM-L6-v2` (local)
- Vector store: SQLite database (`rag_vectors.db`)
- LLM: OpenAI GPT-3.5 (can be replaced with Ollama / local HF model)
- Language: Python 3

## 🚀 How to Set Up & Run

1. (Optional) Create virtual environment
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Ensure there are text/markdown files in the `data/` folder.
4. Build the RAG database:

```bash
python build_db.py
```

5. Set environment variables:

```bash
# Linux/macOS
export TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
export OPENAI_API_KEY="YOUR_OPENAI_KEY"

# Windows (PowerShell)
setx TELEGRAM_BOT_TOKEN "YOUR_TELEGRAM_BOT_TOKEN"
setx OPENAI_API_KEY "YOUR_OPENAI_KEY"
```

6. Run the bot:

```bash
python app.py
```

Then in Telegram:

```text
/start
/ask What is data science?
```

## 💡 RAG System Design (Summary)

- `build_db.py`:
  - Loads documents from `/data`
  - Splits into chunks
  - Embeds chunks using MiniLM
  - Stores chunks + embeddings in SQLite (`rag_vectors.db`)

- `rag_utils.py`:
  - Embeds incoming user query
  - Computes cosine similarity vs stored embeddings
  - Retrieves top-k chunks
  - Builds context string
  - Calls LLM (if key is set) or returns context only

- `app.py`:
  - Telegram bot interface with `/start`, `/help`, `/ask`

This is a complete Mini-RAG implementation matching the **Telegram + Mini-RAG Only** assignment.
