"""Structured memory for GUPPI slice 1: exchanges as queryable SQLite rows, not a chat log.

Per-operation connections (not cached) — Streamlit reruns on every interaction and a
cached sqlite3 connection is bound to its creating thread; short-lived connections
sidestep the thread-affinity error for a single-user local app.
"""
import sqlite3
from datetime import datetime, timezone

DB_PATH = "guppi.db"


def init(path=DB_PATH):
    with sqlite3.connect(path) as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS exchanges (
                 id            INTEGER PRIMARY KEY,
                 timestamp     TEXT NOT NULL,
                 model         TEXT NOT NULL,
                 user_message  TEXT NOT NULL,
                 llm_reply     TEXT NOT NULL
               )"""
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_exchanges_timestamp ON exchanges(timestamp)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_exchanges_model     ON exchanges(model)")


def add(model, user_message, llm_reply, path=DB_PATH):
    ts = datetime.now(timezone.utc).isoformat()
    with sqlite3.connect(path) as conn:
        conn.execute(
            "INSERT INTO exchanges (timestamp, model, user_message, llm_reply) VALUES (?, ?, ?, ?)",
            (ts, model, user_message, llm_reply),
        )


def recent(limit=20, path=DB_PATH):
    with sqlite3.connect(path) as conn:
        rows = conn.execute(
            "SELECT timestamp, model, user_message, llm_reply FROM exchanges ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(zip(("timestamp", "model", "user_message", "llm_reply"), r)) for r in rows]


def search(query, limit=10, path=DB_PATH):
    """Keyword recall over user_message/llm_reply — the recall tool's query path (slice 2)."""
    like = f"%{query}%"
    with sqlite3.connect(path) as conn:
        rows = conn.execute(
            "SELECT timestamp, model, user_message, llm_reply FROM exchanges "
            "WHERE user_message LIKE ? OR llm_reply LIKE ? ORDER BY id DESC LIMIT ?",
            (like, like, limit),
        ).fetchall()
    return [dict(zip(("timestamp", "model", "user_message", "llm_reply"), r)) for r in rows]


def demo():
    """Runnable check: insert a row and read it back, fields intact; search hits and misses."""
    import os
    import tempfile

    path = os.path.join(tempfile.mkdtemp(), "demo.db")
    init(path)
    add("ollama/llama3.2", "my dog's name is Biscuit", "nice to meet Biscuit", path=path)
    rows = recent(path=path)
    assert len(rows) == 1, f"expected 1 row, got {len(rows)}"
    r = rows[0]
    assert r["model"] == "ollama/llama3.2", r
    assert r["user_message"] == "my dog's name is Biscuit", r
    assert r["llm_reply"] == "nice to meet Biscuit", r
    assert r["timestamp"], "timestamp missing"

    hits = search("Biscuit", path=path)
    assert len(hits) == 1 and hits[0]["user_message"] == r["user_message"], hits
    assert search("nothing-matches-this", path=path) == [], "miss should return []"
    print("store.demo() OK:", r)


if __name__ == "__main__":
    demo()
