"""Habit entry upsert operations."""

import json
from datetime import datetime

from storage.db import execute, query_one
from services.habit_service import get_habit_by_id
from services.timer_service import accumulate_timer
from utils.validators import validate_entry_value


def upsert_entry(habit_id, entry_date, value):
    """Insert or update a habit entry.
    
    One entry per habit per date. Value is validated against habit type and meta.
    
    Args:
        habit_id: UUID string
        entry_date: ISO date string (YYYY-MM-DD)
        value: Entry value (type depends on habit type)
    
    Raises:
        ValueError: If habit not found, archived, or value invalid
    """
    # 1. Fetch habit
    habit = get_habit_by_id(habit_id)

    if not habit:
        raise ValueError("Habit not found")

    # 2. Check if habit is archived
    if habit.get("archived") == 1:
        raise ValueError("Cannot log entry for archived habit")

    # 3. Validate value
    validate_entry_value(habit["type"], habit["meta"], value)

    now = datetime.utcnow().isoformat()

    # Convert value to string for DB storage
    stored_value = str(value) if value is not None else None

    # 4. Check if entry exists
    existing = query_one("""
        SELECT id FROM habit_entries
        WHERE habit_id = ? AND entry_date = ?
    """, (habit_id, entry_date))

    if existing:
        # Update existing entry
        execute("""
            UPDATE habit_entries
            SET value = ?, updated_at = ?
            WHERE habit_id = ? AND entry_date = ?
        """, (stored_value, now, habit_id, entry_date))
    else:
        # Insert new entry
        execute("""
            INSERT INTO habit_entries
            (habit_id, entry_date, value, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        """, (habit_id, entry_date, stored_value, now, now))


def add_timer_session(habit_id, entry_date, seconds):
    """Add seconds to a timer habit entry.
    
    Accumulates timer across multiple sessions. Timer entries use separate
    accumulation logic instead of generic upsert_entry().
    
    Args:
        habit_id: UUID string
        entry_date: ISO date string (YYYY-MM-DD)
        seconds: Integer seconds to add
    
    Raises:
        ValueError: If habit not found, archived, or is not a timer type
    """
    # 1. Fetch habit
    habit = get_habit_by_id(habit_id)

    if not habit:
        raise ValueError("Habit not found")

    # 2. Check if habit is archived
    if habit.get("archived") == 1:
        raise ValueError("Cannot log entry for archived habit")

    if habit["type"] != "timer":
        raise ValueError("add_timer_session only works with timer habits")

    now = datetime.utcnow().isoformat()

    # 3. Fetch existing entry
    existing = query_one("""
        SELECT value FROM habit_entries
        WHERE habit_id = ? AND entry_date = ?
    """, (habit_id, entry_date))

    # 4. Accumulate timer
    existing_value = existing["value"] if existing else None
    new_value = accumulate_timer(existing_value, seconds)

    # 5. Upsert with new accumulated value
    if existing:
        execute("""
            UPDATE habit_entries
            SET value = ?, updated_at = ?
            WHERE habit_id = ? AND entry_date = ?
        """, (new_value, now, habit_id, entry_date))
    else:
        execute("""
            INSERT INTO habit_entries
            (habit_id, entry_date, value, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        """, (habit_id, entry_date, new_value, now, now))
