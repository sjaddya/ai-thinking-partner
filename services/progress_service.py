"""Progress aggregation and daily summary."""

from datetime import datetime
from storage.db import query_all
from services.habit_service import list_habits
from services.completion_service import is_entry_complete
from services.streak_service import _is_expected_date


def get_daily_progress(date):
    """Get daily completion summary for all active habits.
    
    Only counts habits that are expected on the given date based on frequency.
    
    Args:
        date: ISO date string (YYYY-MM-DD)
    
    Returns:
        Dict with:
        - date: ISO date string
        - total: Total number of habits expected today
        - completed: Number of completed habits
        - percentage: Completion percentage (0-100)
        - details: List of habit completion details
    """
    # 1. Fetch all active habits
    habits = list_habits()

    # 2. Parse date for frequency checking
    try:
        date_obj = datetime.fromisoformat(date).date()
    except ValueError:
        raise ValueError(f"Invalid date format: {date}. Must be ISO format (YYYY-MM-DD)")

    # 3. Fetch all entries for that date
    rows = query_all(
        "SELECT habit_id, value FROM habit_entries WHERE entry_date = ?",
        (date,)
    )

    # Convert entries into lookup dict
    entry_lookup = {
        row["habit_id"]: row["value"]
        for row in rows
    }

    total = 0
    completed = 0
    details = []

    # 4. Evaluate each habit
    for habit in habits:
        habit_id = habit["id"]
        
        # Check if this date is expected for this habit based on frequency
        if not _is_expected_date(habit, date_obj):
            # Skip habits that don't have entries expected on this date
            continue

        total += 1
        value = entry_lookup.get(habit_id)

        if value is not None:
            complete = is_entry_complete(habit, value)
        else:
            complete = False

        if complete:
            completed += 1

        details.append({
            "habit_id": habit_id,
            "name": habit["name"],
            "type": habit["type"],
            "complete": complete,
            "value": value
        })

    # 5. Calculate percentage
    percentage = 0.0
    if total > 0:
        percentage = round((completed / total) * 100, 2)

    return {
        "date": date,
        "total": total,
        "completed": completed,
        "percentage": percentage,
        "details": details
    }
