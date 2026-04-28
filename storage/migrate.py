import sqlite3

from storage.db import get_connection


def _add_column_safe(connection, table_name, column_name, definition, fallback_definition=None):
    try:
        connection.execute(
            f"ALTER TABLE {table_name} ADD COLUMN {column_name} {definition}"
        )
    except sqlite3.OperationalError as exc:
        message = str(exc).lower()
        if "duplicate column name" in message:
            return

        if fallback_definition and "non-constant default" in message:
            try:
                connection.execute(
                    f"ALTER TABLE {table_name} ADD COLUMN {column_name} {fallback_definition}"
                )
            except sqlite3.OperationalError as fallback_exc:
                if "duplicate column name" not in str(fallback_exc).lower():
                    raise
            return

        raise


def _ensure_habits_columns(connection):
    _add_column_safe(connection, "habits", "name", "TEXT NOT NULL DEFAULT ''")
    _add_column_safe(connection, "habits", "type", "TEXT NOT NULL DEFAULT ''")
    _add_column_safe(connection, "habits", "meta", "TEXT")
    _add_column_safe(connection, "habits", "archived", "INTEGER NOT NULL DEFAULT 0")
    _add_column_safe(
        connection,
        "habits",
        "created_at",
        "TEXT DEFAULT CURRENT_TIMESTAMP",
        fallback_definition="TEXT",
    )
    _add_column_safe(connection, "habits", "category", "TEXT DEFAULT 'General'")
    _add_column_safe(connection, "habits", "frequency", "TEXT DEFAULT 'daily'")


def _ensure_habit_entries_columns(connection):
    _add_column_safe(connection, "habit_entries", "habit_id", "TEXT NOT NULL DEFAULT ''")
    _add_column_safe(connection, "habit_entries", "entry_date", "TEXT NOT NULL DEFAULT ''")
    _add_column_safe(connection, "habit_entries", "value", "TEXT")
    _add_column_safe(
        connection,
        "habit_entries",
        "created_at",
        "TEXT DEFAULT CURRENT_TIMESTAMP",
        fallback_definition="TEXT",
    )
    _add_column_safe(
        connection,
        "habit_entries",
        "updated_at",
        "TEXT DEFAULT CURRENT_TIMESTAMP",
        fallback_definition="TEXT",
    )


def _backfill_defaults(connection):
    connection.execute(
        "UPDATE habits SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL"
    )
    connection.execute("UPDATE habits SET archived = 0 WHERE archived IS NULL")
    connection.execute(
        "UPDATE habit_entries SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL"
    )
    connection.execute(
        "UPDATE habit_entries SET updated_at = CURRENT_TIMESTAMP WHERE updated_at IS NULL"
    )


def run_migrations():
    schema = """
    CREATE TABLE IF NOT EXISTS habits (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        meta TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        archived INTEGER NOT NULL DEFAULT 0,
        category TEXT DEFAULT 'General',
        frequency TEXT DEFAULT 'daily'
    );

    CREATE TABLE IF NOT EXISTS habit_entries (
        id INTEGER PRIMARY KEY,
        habit_id TEXT NOT NULL,
        entry_date TEXT NOT NULL,
        value TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(habit_id, entry_date),
        FOREIGN KEY(habit_id) REFERENCES habits(id)
    );

    CREATE TABLE IF NOT EXISTS journal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entry TEXT NOT NULL DEFAULT '',
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS thoughts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        note TEXT NOT NULL DEFAULT '',
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """

    connection = get_connection()
    try:
        connection.executescript(schema)
        _ensure_habits_columns(connection)
        _ensure_habit_entries_columns(connection)
        _backfill_defaults(connection)
        connection.commit()
    finally:
        connection.close()


if __name__ == "__main__":
    run_migrations()
    print("Migration complete.")
