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


def demo():
    """Runnable check: insert a row and read it back, fields intact."""
    import os
    import tempfile

    path = os.path.join(tempfile.mkdtemp(), "demo.db")
    init(path)
    add("ollama/llama3.2", "hello", "hi there", path=path)
    rows = recent(path=path)
    assert len(rows) == 1, f"expected 1 row, got {len(rows)}"
    r = rows[0]
    assert r["model"] == "ollama/llama3.2", r
    assert r["user_message"] == "hello", r
    assert r["llm_reply"] == "hi there", r
    assert r["timestamp"], "timestamp missing"
    print("store.demo() OK:", r)


if __name__ == "__main__":
    demo()
