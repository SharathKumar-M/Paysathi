from __future__ import annotations
import os
import sqlite3
from pathlib import Path
from datetime import datetime, timezone


def _db_path() -> Path:
    return Path(os.getenv("PAYSAATHI_DB_PATH", "./data/paysaathi.db")).expanduser().resolve()


def connect() -> sqlite3.Connection:
    path = _db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS gym_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                scenario_id TEXT NOT NULL,
                stage TEXT NOT NULL CHECK(stage IN ('before', 'practice', 'after')),
                choice_id TEXT NOT NULL,
                correct INTEGER NOT NULL,
                elapsed_seconds INTEGER NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_gym_session ON gym_attempts(session_id)")


def save_attempt(*, session_id: str, scenario_id: str, stage: str, choice_id: str, correct: bool, elapsed_seconds: int) -> None:
    with connect() as conn:
        conn.execute(
            "INSERT INTO gym_attempts(session_id, scenario_id, stage, choice_id, correct, elapsed_seconds, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (session_id, scenario_id, stage, choice_id, int(correct), elapsed_seconds, datetime.now(timezone.utc).isoformat()),
        )


def get_summary(session_id: str) -> dict:
    with connect() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS total, COALESCE(SUM(correct), 0) AS correct FROM gym_attempts WHERE session_id = ?",
            (session_id,),
        ).fetchone()
        stages = conn.execute(
            "SELECT stage, COUNT(*) AS total FROM gym_attempts WHERE session_id = ? GROUP BY stage",
            (session_id,),
        ).fetchall()
    total = int(row["total"])
    correct = int(row["correct"])
    return {
        "total_attempts": total,
        "correct_attempts": correct,
        "accuracy_percent": round((correct / total) * 100) if total else 0,
        "by_stage": {r["stage"]: int(r["total"]) for r in stages},
    }
