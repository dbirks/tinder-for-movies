import sqlite3
from contextlib import contextmanager
import os

DB_PATH = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")

# Extract file path from DATABASE_URL if needed
def get_db_file_path():
    if DB_PATH.startswith("sqlite:///"):
        return DB_PATH.replace("sqlite:///", "")
    return DB_PATH

@contextmanager
def get_db():
    db_path = get_db_file_path()
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.close()
