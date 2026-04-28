"""Habit streak computation engine."""

from datetime import datetime, timedelta
from storage.db import query_all
from services.habit_service import get_habit_by_id
from services.completion_service import is_entry_complete


def get_current_streak(habit_id):
    """Get current consecutive completion streak.
    
    Counts consecutive completed days from today backward,
    respecting the habit's frequency schedule.
    
    Args:
        habit_id: UUID string
    
    Returns:
        Int - current streak count (0 if incomplete today or yesterday)
    """
    habit = get_habit_by_id(habit_id)
    
    if not habit:
        return 0

    # Fetch all entries for this habit, sorted by date descending
    rows = query_all("""
        SELECT entry_date, value FROM habit_entries
        WHERE habit_id = ?
        ORDER BY entry_date DESC
    """, (habit_id,))

    if not rows:
        return 0

    # Build entry lookup
    entry_lookup = {row["entry_date"]: row["value"] for row in rows}

    # Get today and yesterday for streak detection
    today = datetime.utcnow().date()
    streak = 0
    current_date = today

    # Walk backward from today
    while True:
        # Check if this date is within expected frequency
        if not _is_expected_date(habit, current_date):
            current_date -= timedelta(days=1)
            continue

        # Check if entry exists and is complete
        date_str = current_date.isoformat()
        
        if date_str not in entry_lookup:
            # Missing expected entry breaks streak
            break

        value = entry_lookup[date_str]
        if not is_entry_complete(habit, value):
            # Incomplete entry breaks streak
            break

        streak += 1
        current_date -= timedelta(days=1)

        # Safety: don't go back more than a year
        if (today - current_date).days > 365:
            break

    return streak


def get_longest_streak(habit_id):
    """Get longest consecutive completion streak in history.
    
    Scans entire habit history for the longest streak,
    respecting the habit's frequency schedule.
    
    Args:
        habit_id: UUID string
    
    Returns:
        Int - longest streak count (0 if no completions)
    """
    habit = get_habit_by_id(habit_id)
    
    if not habit:
        return 0

    # Fetch all entries for this habit, sorted by date ascending
    rows = query_all("""
        SELECT entry_date, value FROM habit_entries
        WHERE habit_id = ?
        ORDER BY entry_date ASC
    """, (habit_id,))

    if not rows:
        return 0

    # Build sorted date list
    dates = sorted([row["entry_date"] for row in rows])
    entry_lookup = {row["entry_date"]: row["value"] for row in rows}

    longest = 0
    current = 0
    last_date = None

    for date_str in dates:
        current_date = datetime.fromisoformat(date_str).date()

        # Check if date is expected
        if not _is_expected_date(habit, current_date):
            continue

        # Check if entry is complete
        value = entry_lookup[date_str]
        
        if not is_entry_complete(habit, value):
            # Reset streak on incomplete entry
            current = 0
            last_date = None
            continue

        # Check for continuity
        if last_date is None:
            # First entry in potential streak
            current = 1
        else:
            days_diff = (current_date - last_date).days
            
            # Count only consecutive expected dates
            expected_days = 0
            check_date = last_date + timedelta(days=1)
            
            while check_date <= current_date:
                if _is_expected_date(habit, check_date):
                    expected_days += 1
                check_date += timedelta(days=1)

            if expected_days == days_diff:
                # Consecutive expected dates
                current += 1
            else:
                # Gap in expected dates breaks streak
                current = 1

        longest = max(longest, current)
        last_date = current_date

    return longest


def _is_expected_date(habit, date):
    """Check if a date is expected based on habit frequency.
    
    Args:
        habit: Habit dict with frequency and meta
        date: datetime.date object
    
    Returns:
        Boolean - True if this date should have an entry
    """
    frequency = habit.get("frequency", "daily")

    if frequency == "daily":
        return True

    elif frequency == "weekly":
        # Check if this day of week is in meta
        # Default to all days if not specified
        frequency_days = habit.get("meta", {}).get("frequency_days", list(range(7)))
        return date.weekday() in frequency_days

    elif frequency == "custom":
        # Check if this day of month is in meta
        frequency_days = habit.get("meta", {}).get("frequency_days", list(range(1, 32)))
        return date.day in frequency_days

    return True
