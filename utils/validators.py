"""Habit type validation system."""

from utils.constants import HABIT_TYPES, HABIT_CATEGORIES, HABIT_FREQUENCIES


def validate_habit_type_and_meta(habit_type, meta):
    """Validate habit type and metadata configuration.
    
    Raises ValueError if configuration is invalid.
    """
    if habit_type not in HABIT_TYPES:
        raise ValueError(f"Unsupported habit type: {habit_type}. Must be one of {HABIT_TYPES}")

    if not isinstance(meta, dict):
        raise ValueError("Meta must be a dictionary")

    if habit_type == "boolean":
        if meta:
            raise ValueError("Boolean type does not use meta")

    elif habit_type == "count":
        if "unit_label" in meta and not isinstance(meta["unit_label"], str):
            raise ValueError("unit_label must be string")
        
        if "target" in meta:
            if not isinstance(meta["target"], int) or meta["target"] <= 0:
                raise ValueError("target must be a positive integer")

    elif habit_type == "duration":
        if meta.get("unit") not in ["minutes", "hours"]:
            raise ValueError("Duration requires unit: minutes or hours")
        
        if "target" in meta:
            if not isinstance(meta["target"], int) or meta["target"] <= 0:
                raise ValueError("target must be a positive integer")

    elif habit_type == "time_of_day":
        if meta:
            raise ValueError("time_of_day does not use meta")

    elif habit_type == "scale":
        scale_min = meta.get("scale_min")
        scale_max = meta.get("scale_max")

        if scale_min is None or scale_max is None:
            raise ValueError("Scale requires scale_min and scale_max")

        if not (scale_min < scale_max):
            raise ValueError("scale_min must be less than scale_max")

    elif habit_type == "signed_scale":
        scale_min = meta.get("scale_min")
        scale_max = meta.get("scale_max")

        if scale_min is None or scale_max is None:
            raise ValueError("Signed scale requires scale_min and scale_max")

        if not (scale_min < scale_max):
            raise ValueError("Invalid signed scale range")

    elif habit_type == "note":
        if meta:
            raise ValueError("note type does not use meta")

    elif habit_type == "timer":
        minimum_minutes = meta.get("minimum_minutes")

        if not isinstance(minimum_minutes, int) or minimum_minutes <= 0:
            raise ValueError("Timer requires minimum_minutes > 0")
        
        if "target" in meta:
            if not isinstance(meta["target"], int) or meta["target"] <= 0:
                raise ValueError("target must be a positive integer (minutes)")


def validate_entry_value(habit_type, meta, value):
    """Validate daily entry value for a habit.
    
    Raises ValueError if value is invalid for the habit type.
    """
    if habit_type == "boolean":
        if value not in (0, 1):
            raise ValueError("Boolean must be 0 or 1")

    elif habit_type == "count":
        if not isinstance(value, int) or value < 0:
            raise ValueError("Count must be integer >= 0")

    elif habit_type == "duration":
        if not isinstance(value, int) or value < 0:
            raise ValueError("Duration must be integer >= 0")

    elif habit_type == "time_of_day":
        if value is None:
            return

        if not isinstance(value, str) or len(value) != 5:
            raise ValueError("Time must be HH:MM")

    elif habit_type == "scale":
        if not (meta["scale_min"] <= value <= meta["scale_max"]):
            raise ValueError("Scale out of range")

    elif habit_type == "signed_scale":
        if not (meta["scale_min"] <= value <= meta["scale_max"]):
            raise ValueError("Signed scale out of range")

    elif habit_type == "note":
        if not isinstance(value, str):
            raise ValueError("Note must be string")

    elif habit_type == "timer":
        if not isinstance(value, str):
            raise ValueError("Timer must be HH:MM:SS string")

        parts = value.split(":")
        if len(parts) != 3:
            raise ValueError("Timer format must be HH:MM:SS")


def validate_frequency(frequency, meta):
    """Validate habit frequency and metadata.
    
    For frequency=custom, meta must contain frequency_days list.
    
    Args:
        frequency: One of HABIT_FREQUENCIES
        meta: Habit metadata dict
    
    Raises:
        ValueError: If frequency or custom config invalid
    """
    if frequency not in HABIT_FREQUENCIES:
        raise ValueError(f"Unsupported frequency: {frequency}. Must be one of {HABIT_FREQUENCIES}")

    if frequency == "custom":
        if "frequency_days" not in meta:
            raise ValueError("Custom frequency requires 'frequency_days' in metadata")

        frequency_days = meta["frequency_days"]

        if not isinstance(frequency_days, list):
            raise ValueError("frequency_days must be a list")

        if not frequency_days or len(frequency_days) == 0:
            raise ValueError("frequency_days cannot be empty")

        # Validate each day is integer 0-6 (Sunday=0, Saturday=6)
        for day in frequency_days:
            if not isinstance(day, int) or not (0 <= day <= 6):
                raise ValueError("frequency_days must contain integers 0-6")


def validate_category(category):
    """Validate habit category.
    
    Category must be one of the predefined HABIT_CATEGORIES.
    
    Args:
        category: Category string
    
    Raises:
        ValueError: If category invalid or not in allowed list
    """
    if not isinstance(category, str):
        raise ValueError("Category must be a string")

    if not category or len(category.strip()) == 0:
        raise ValueError("Category cannot be empty")

    if category not in HABIT_CATEGORIES:
        raise ValueError(f"Invalid category: {category}. Must be one of {HABIT_CATEGORIES}")
