"""Completion status computation."""

from services.timer_service import is_timer_complete


def is_entry_complete(habit, value):
    """Determine if an entry marks the habit as complete.
    
    Assumes the provided date has already been validated against frequency.
    Only evaluates the value itself against completion criteria.
    
    Completion rules vary by habit type:
    - boolean: value == "1"
    - count: if target exists → value >= target, else → value > 0
    - duration: if target exists → value >= target, else → value > 0
    - timer: if target exists → reaches target (minutes), else → reaches minimum_minutes
    - scale: any valid value means complete
    - signed_scale: any valid value means complete
    - note: non-empty string
    - time_of_day: not None
    
    Args:
        habit: Habit dict with type and meta
        value: Entry value as string (or None for optional types)
    
    Returns:
        Boolean - True if entry marks habit complete for the day
    """
    habit_type = habit["type"]
    meta = habit["meta"]

    if habit_type == "boolean":
        return value == "1"

    elif habit_type == "count":
        count_value = int(value)
        if "target" in meta:
            return count_value >= meta["target"]
        return count_value > 0

    elif habit_type == "duration":
        duration_value = int(value)
        if "target" in meta:
            return duration_value >= meta["target"]
        return duration_value > 0

    elif habit_type == "timer":
        return is_timer_complete(meta, value)

    elif habit_type == "scale":
        # Any valid scale value means complete
        return value is not None

    elif habit_type == "signed_scale":
        # Any valid signed scale value means complete
        return value is not None

    elif habit_type == "note":
        # Non-empty string means complete
        return isinstance(value, str) and len(value) > 0

    elif habit_type == "time_of_day":
        # Non-None time means complete
        return value is not None

    return False
