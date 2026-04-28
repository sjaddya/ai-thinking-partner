"""Progress API endpoints."""

from fastapi import APIRouter
from services.progress_service import get_daily_progress
from api.schemas import ProgressResponse

router = APIRouter()


@router.get("/", response_model=ProgressResponse)
def daily_progress(date: str):
    """Get daily progress summary for a date."""
    return get_daily_progress(date)
