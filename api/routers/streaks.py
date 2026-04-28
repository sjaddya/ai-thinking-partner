"""Streak API endpoints."""

from fastapi import APIRouter, HTTPException
from services.streak_service import get_current_streak, get_longest_streak
from api.schemas import StreakResponse

router = APIRouter()


@router.get("/{habit_id}/current", response_model=StreakResponse)
def get_current_streak_endpoint(habit_id: str):
    """Get current consecutive completion streak for a habit."""
    try:
        streak = get_current_streak(habit_id)
        return StreakResponse(habit_id=habit_id, current_streak=streak)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{habit_id}/longest", response_model=StreakResponse)
def get_longest_streak_endpoint(habit_id: str):
    """Get longest consecutive completion streak for a habit."""
    try:
        streak = get_longest_streak(habit_id)
        return StreakResponse(habit_id=habit_id, longest_streak=streak)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
