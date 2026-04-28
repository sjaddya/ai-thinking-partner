"""Monthly progress API endpoints."""

from fastapi import APIRouter, HTTPException
from services.monthly_service import get_monthly_progress
from api.schemas import MonthlyResponse

router = APIRouter()


@router.get("/", response_model=MonthlyResponse)
def get_monthly_progress_endpoint(year: int, month: int):
    """Get monthly completion summary for all active habits.
    
    Args:
        year: Integer year (e.g., 2026)
        month: Integer month (1-12)
    
    Returns:
        Dict with year, month, and daily breakdown
    """
    try:
        progress = get_monthly_progress(year, month)
        return progress
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
