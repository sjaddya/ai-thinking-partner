"""Entries API endpoints."""

from fastapi import APIRouter, HTTPException
from services.entry_service import upsert_entry, add_timer_session
from api.schemas import EntryCreate, TimerSession, StatusResponse

router = APIRouter()


@router.post("/", response_model=StatusResponse)
def create_entry(entry: EntryCreate):
    """Log a habit entry."""
    try:
        upsert_entry(entry.habit_id, entry.date, entry.value)
        return StatusResponse(status="ok")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/timer", response_model=StatusResponse)
def add_timer(entry: TimerSession):
    """Add seconds to a timer habit session."""
    try:
        add_timer_session(entry.habit_id, entry.date, entry.seconds)
        return StatusResponse(status="ok")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
