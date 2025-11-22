# Mini-RAG Telegram Bot – Architecture Diagram

```text
+------------------+        +---------------------+
|  Telegram User   |        |   Local Machine     |
+---------+--------+        +----------+----------+
          |                            |
          |  /ask <query>              |
          +--------------------------->|
                                       |
                          +------------v-------------+
                          |   Telegram Bot (app.py)  |
                          |  - Handles /start        |
                          |  - Handles /help         |
                          |  - Handles /ask          |
                          +------------+-------------+
                                       |
                                       v
                          +------------+-------------+
                          |   RAG Utils (rag_utils)  |
                          |  - Embed query           |
                          |  - Retrieve top-k chunks |
                          |  - Build context         |
                          |  - Call LLM              |
                          +------------+-------------+
                                       |
                      uses             |
         +-----------------------------v----------------------+
         |                  RAG Store (SQLite)                |
         |                  rag_vectors.db                    |
         |  - chunks(id, doc_name, text, embedding BLOB)      |
         +-----------------------------+----------------------+
                                       ^
                                       |
                          +------------+-------------+
                          |   build_db.py            |
                          |  - Load /data docs       |
                          |  - Chunk text            |
                          |  - Embed with MiniLM     |
                          |  - Insert into SQLite    |
                          +--------------------------+
```
