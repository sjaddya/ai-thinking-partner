"""Habit CRUD operations."""

import json
from uuid import uuid4
from datetime import datetime

from storage.db import execute, query_one, query_all
from utils.validators import validate_habit_type_and_meta, validate_frequency, validate_category


def create_habit(name, habit_type, meta, category="General", frequency="daily"):
    """Create a new habit.
    
    Args:
        name: Habit name
        habit_type: One of HABIT_TYPES from utils.constants
        meta: Metadata dict (validated against type)
        category: Habit category (default: "General")
        frequency: Frequency type - "daily", "weekly", or "custom" (default: "daily")
    
    Returns:
        habit_id: UUID string
    
    Raises:
        ValueError: If type, meta, category, or frequency invalid
    """
    validate_habit_type_and_meta(habit_type, meta)
    validate_frequency(frequency, meta)
    validate_category(category)

    habit_id = str(uuid4())
    created_at = datetime.utcnow().isoformat()

    execute("""
        INSERT INTO habits (id, name, type, meta, created_at, archived, category, frequency)
        VALUES (?, ?, ?, ?, ?, 0, ?, ?)
    """, (
        habit_id,
        name,
        habit_type,
        json.dumps(meta),
        created_at,
        category,
        frequency
    ))

    return habit_id


def get_habit_by_id(habit_id):
    """Get a habit by ID.
    
    Args:
        habit_id: UUID string
    
    Returns:
        Habit dict with meta as dict, or None if not found
    """
    row = query_one(
        "SELECT * FROM habits WHERE id = ? AND archived = 0",
        (habit_id,)
    )

    if not row:
        return None

    habit = dict(row)
    habit["meta"] = json.loads(habit["meta"])

    return habit


def list_habits():
    """List all non-archived habits.
    
    Returns:
        List of habit dicts with meta as dict
    """
    rows = query_all(
        "SELECT * FROM habits WHERE archived = 0"
    )

    habits = []

    for row in rows:
        habit = dict(row)
        habit["meta"] = json.loads(habit["meta"])
        habits.append(habit)

    return habits


def update_habit_name_meta(habit_id, new_name, new_meta):
    """Update habit name and metadata.
    
    Args:
        habit_id: UUID string
        new_name: Updated name
        new_meta: Updated metadata dict
    
    Raises:
        ValueError: If habit not found or meta invalid
    """
    habit = get_habit_by_id(habit_id)

    if not habit:
        raise ValueError("Habit not found")

    # Type cannot change - validate against existing type
    validate_habit_type_and_meta(habit["type"], new_meta)

    execute("""
        UPDATE habits
        SET name = ?, meta = ?
        WHERE id = ?
    """, (
        new_name,
        json.dumps(new_meta),
        habit_id
    ))


def archive_habit(habit_id):
    """Archive a habit (soft delete).
    
    Args:
        habit_id: UUID string
    """
    execute("""
        UPDATE habits
        SET archived = 1
        WHERE id = ?
    """, (habit_id,))


def update_habit_category_and_frequency(habit_id, category=None, frequency=None):
    """Update habit category and/or frequency.
    
    Args:
        habit_id: UUID string
        category: New category (optional)
        frequency: New frequency - "daily", "weekly", or "custom" (optional)
    
    Raises:
        ValueError: If habit not found or inputs invalid
    """
    habit = get_habit_by_id(habit_id)

    if not habit:
        raise ValueError("Habit not found")

    # Validate inputs if provided
    if category is not None:
        validate_category(category)
    else:
        category = habit.get("category", "General")

    if frequency is not None:
        validate_frequency(frequency, habit["meta"])
    else:
        frequency = habit.get("frequency", "daily")

    execute("""
        UPDATE habits
        SET category = ?, frequency = ?
        WHERE id = ?
    """, (category, frequency, habit_id))


def unarchive_habit(habit_id):
    """Restore an archived habit.
    
    Args:
        habit_id: UUID string
    """
    execute("""
        UPDATE habits
        SET archived = 0
        WHERE id = ?
    """, (habit_id,))


def delete_habit_permanently(habit_id):
    """Permanently delete a habit and all its entries.
    
    Must delete entries first due to foreign key constraint.
    
    Args:
        habit_id: UUID string
    """
    execute("DELETE FROM habit_entries WHERE habit_id = ?", (habit_id,))
    execute("DELETE FROM habits WHERE id = ?", (habit_id,))


def list_archived_habits():
    """List all archived habits.
    
    Returns:
        List of habit dicts with meta as dict
    """
    rows = query_all(
        "SELECT * FROM habits WHERE archived = 1"
    )

    habits = []

    for row in rows:
        habit = dict(row)
        habit["meta"] = json.loads(habit["meta"])
        habits.append(habit)

    return habits
