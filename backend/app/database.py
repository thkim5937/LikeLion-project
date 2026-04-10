"""
database.py  –  Sets up and connects to our SQLite database.

SQLite stores everything in a single file (todo.db).
This module gives the rest of the app two things:
  1. get_connection()  – open a connection to the database
  2. init_db()         – create the "todos" table if it doesn't exist yet
"""

import sqlite3
from pathlib import Path

# ---------------------------------------------------------------------------
# Where the database file lives (next to the "app/" folder).
# Path(__file__)  = this file's location  (database.py)
# .resolve()      = full absolute path
# .parent.parent  = go up two folders: app/ → backend/
# So DB_PATH = backend/todo.db
# ---------------------------------------------------------------------------
DB_PATH = Path(__file__).resolve().parent.parent / "todo.db"


def get_connection() -> sqlite3.Connection:
    """
    Open a connection to the SQLite database.

    connection.row_factory = sqlite3.Row
      ↑ This lets us access columns by NAME (row["title"])
        instead of by number (row[1]).  Much easier to read!
    """
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    """
    Create the todos table if it doesn't already exist.
    Called once when the server starts up.

    Column breakdown:
      id          – unique number assigned automatically (1, 2, 3, …)
      title       – the todo's name (required)
      description – optional extra details (defaults to empty string)
      completed   – 0 = not done, 1 = done  (SQLite has no true bool)
      due_date    – optional deadline stored as an ISO 8601 text string
                    e.g. "2026-03-15T09:00:00"   (NULL if no deadline)
    """
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                completed INTEGER NOT NULL DEFAULT 0,
                due_date TEXT NULL
            )
            """
        )

        # ------------------------------------------------------------------
        # MIGRATION: If the table already existed (from an older version)
        # it might not have the due_date column yet.  PRAGMA table_info
        # tells us what columns exist so we can add it if missing.
        # ------------------------------------------------------------------
        cursor = connection.execute("PRAGMA table_info(todos)")
        columns = [row[1] for row in cursor.fetchall()]  # list of column names
        if "due_date" not in columns:
            connection.execute("ALTER TABLE todos ADD COLUMN due_date TEXT NULL")

        connection.commit()  # save changes to disk
