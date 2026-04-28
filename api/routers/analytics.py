"""Analytics API endpoints."""

from fastapi import APIRouter, HTTPException
from services.analytics_service import get_habit_stats
from api.schemas import AnalyticsResponse

router = APIRouter()


@router.get("/{habit_id}", response_model=AnalyticsResponse)
def get_habit_stats_endpoint(habit_id: str, start_date: str, end_date: str):
    """Get aggregated statistics for a habit over a date range.
    
    Args:
        habit_id: UUID string
        start_date: ISO date string (YYYY-MM-DD)
        end_date: ISO date string (YYYY-MM-DD)
    
    Returns:
        Dict with total, average, days_logged, and type-specific fields
    """
    try:
        stats = get_habit_stats(habit_id, start_date, end_date)
        return stats
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
