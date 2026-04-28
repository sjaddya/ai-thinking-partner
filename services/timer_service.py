"""Timer accumulation and completion logic."""


def seconds_to_hhmmss(total_seconds):
    """Convert seconds to HH:MM:SS format.
    
    Args:
        total_seconds: Integer seconds
    
    Returns:
        String in format HH:MM:SS
    """
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def hhmmss_to_seconds(value):
    """Convert HH:MM:SS string to seconds.
    
    Args:
        value: String in format HH:MM:SS
    
    Returns:
        Integer seconds
    """
    h, m, s = map(int, value.split(":"))
    return h * 3600 + m * 60 + s


def accumulate_timer(existing_value, seconds_to_add):
    """Accumulate timer by adding seconds to existing value.
    
    Args:
        existing_value: HH:MM:SS string or None
        seconds_to_add: Integer seconds to add
    
    Returns:
        New value as HH:MM:SS string
    """
    current_seconds = 0

    if existing_value:
        current_seconds = hhmmss_to_seconds(existing_value)

    new_total = current_seconds + seconds_to_add
    return seconds_to_hhmmss(new_total)


def is_timer_complete(meta, value):
    """Check if timer has reached its target.
    
    If target exists in meta, use that. Otherwise, use minimum_minutes.
    
    Args:
        meta: Habit metadata dict with minimum_minutes and optional target
        value: HH:MM:SS string
    
    Returns:
        Boolean - True if total minutes >= target (or minimum_minutes if no target)
    """
    total_seconds = hhmmss_to_seconds(value)
    total_minutes = total_seconds // 60
    
    # Use target if it exists, otherwise fall back to minimum_minutes
    required_minutes = meta.get("target") or meta["minimum_minutes"]
    
    return total_minutes >= required_minutes
