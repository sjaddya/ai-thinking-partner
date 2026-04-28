import sqlite3
from pathlib import Path

from config import Config

# Database path configuration
DB_PATH = Path(Config.DATABASE_PATH)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_connection():
    """Get a stable database connection with proper settings."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def execute(query, params=()):
    """Execute a query (INSERT, UPDATE, DELETE) and commit."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()


def query_one(query, params=()):
    """Execute a query and return a single row."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    row = cursor.fetchone()
    conn.close()
    return row


def query_all(query, params=()):
    """Execute a query and return all rows."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows
