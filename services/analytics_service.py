"""Habit analytics and statistics engine."""

from datetime import datetime
from storage.db import query_all
from services.habit_service import get_habit_by_id
from services.completion_service import is_entry_complete
from services.timer_service import hhmmss_to_seconds


def get_habit_stats(habit_id, start_date, end_date):
    """Get aggregated statistics for a habit over a date range.
    
    Aggregation rules by habit type:
    - count: sum all values
    - duration: sum all values
    - timer: convert HH:MM:SS to seconds and sum
    - scale: average all values
    - signed_scale: average all values
    - boolean: count of 1s (true completions)
    - note: days logged (count of non-empty entries)
    - time_of_day: days logged (count of non-empty entries)
    
    Args:
        habit_id: UUID string
        start_date: ISO date string (YYYY-MM-DD)
        end_date: ISO date string (YYYY-MM-DD)
    
    Returns:
        Dict with:
        - total: Aggregated total (sum for numeric, count for boolean/note/time/time_of_day)
        - average: Average value (for scale/signed_scale), None for others
        - days_logged: Number of days with entries
        - unit: Original unit (if applicable)
    
    Raises:
        ValueError: If habit not found or dates invalid
    """
    habit = get_habit_by_id(habit_id)
    
    if not habit:
        raise ValueError("Habit not found")

    # Validate dates
    try:
        start = datetime.fromisoformat(start_date).date()
        end = datetime.fromisoformat(end_date).date()
    except ValueError:
        raise ValueError("Dates must be in ISO format (YYYY-MM-DD)")

    if start > end:
        raise ValueError("start_date must be before or equal to end_date")

    # Fetch all entries in date range
    rows = query_all("""
        SELECT entry_date, value FROM habit_entries
        WHERE habit_id = ? AND entry_date >= ? AND entry_date <= ?
        ORDER BY entry_date ASC
    """, (habit_id, start_date, end_date))

    if not rows:
        return {
            "total": 0,
            "average": None,
            "days_logged": 0
        }

    habit_type = habit["type"]
    meta = habit["meta"]
    values = [row["value"] for row in rows]
    days_logged = len(values)

    # Aggregate based on type
    if habit_type == "count":
        total = sum(int(v) for v in values)
        return {
            "total": total,
            "average": total / days_logged if days_logged > 0 else 0,
            "days_logged": days_logged,
            "unit": meta.get("unit_label", "count")
        }

    elif habit_type == "duration":
        total = sum(int(v) for v in values)
        unit = meta.get("unit", "minutes")
        return {
            "total": total,
            "average": total / days_logged if days_logged > 0 else 0,
            "days_logged": days_logged,
            "unit": unit
        }

    elif habit_type == "timer":
        # Convert HH:MM:SS to seconds and sum
        total_seconds = sum(hhmmss_to_seconds(v) for v in values)
        total_minutes = total_seconds / 60
        return {
            "total": total_seconds,
            "average": total_seconds / days_logged if days_logged > 0 else 0,
            "days_logged": days_logged,
            "unit": "seconds",
            "minutes_total": total_minutes
        }

    elif habit_type == "scale":
        values_numeric = [int(v) for v in values]
        total = sum(values_numeric)
        average = total / days_logged if days_logged > 0 else 0
        return {
            "total": total,
            "average": round(average, 2),
            "days_logged": days_logged,
            "scale_min": meta.get("scale_min"),
            "scale_max": meta.get("scale_max")
        }

    elif habit_type == "signed_scale":
        values_numeric = [int(v) for v in values]
        total = sum(values_numeric)
        average = total / days_logged if days_logged > 0 else 0
        return {
            "total": total,
            "average": round(average, 2),
            "days_logged": days_logged,
            "scale_min": meta.get("scale_min"),
            "scale_max": meta.get("scale_max")
        }

    elif habit_type == "boolean":
        # Count true completions (value == "1")
        true_count = sum(1 for v in values if v == "1")
        return {
            "total": true_count,
            "average": None,
            "days_logged": days_logged,
            "completion_rate": round((true_count / days_logged * 100) if days_logged > 0 else 0, 2)
        }

    elif habit_type == "note":
        # Count days with non-empty notes
        notes_count = sum(1 for v in values if v and len(v) > 0)
        return {
            "total": notes_count,
            "average": None,
            "days_logged": days_logged
        }

    elif habit_type == "time_of_day":
        # Count days with time recorded
        times_count = sum(1 for v in values if v)
        return {
            "total": times_count,
            "average": None,
            "days_logged": days_logged
        }

    return {
        "total": 0,
        "average": None,
        "days_logged": days_logged
    }
