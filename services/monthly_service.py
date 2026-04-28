"""Monthly progress aggregation service."""

from datetime import datetime, date, timedelta
from services.progress_service import get_daily_progress


def get_monthly_progress(year, month):
    """Get monthly completion summary for all active habits.
    
    Args:
        year: Integer year (e.g., 2026)
        month: Integer month (1-12)
    
    Returns:
        Dict with:
        - year: Integer year
        - month: Integer month
        - days: List of daily summaries, each with:
          - date: ISO date string
          - completed: Number of completed habits
          - total: Total number of active habits
    
    Raises:
        ValueError: If year or month invalid
    """
    # Validate month
    if not (1 <= month <= 12):
        raise ValueError(f"Month must be 1-12, got {month}")

    # Validate year (reasonable range)
    if year < 1900 or year > 2100:
        raise ValueError(f"Year must be between 1900 and 2100, got {year}")

    # Get first and last day of month
    first_day = date(year, month, 1)
    
    # Last day calculation
    if month == 12:
        last_day = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = date(year, month + 1, 1) - timedelta(days=1)

    days = []
    current_date = first_day

    # Iterate through each day in the month
    while current_date <= last_day:
        date_str = current_date.isoformat()
        
        # Get daily progress
        daily = get_daily_progress(date_str)
        
        # Add to results with just the summary fields
        days.append({
            "date": date_str,
            "completed": daily["completed"],
            "total": daily["total"]
        })

        current_date += timedelta(days=1)

    return {
        "year": year,
        "month": month,
        "days": days
    }
