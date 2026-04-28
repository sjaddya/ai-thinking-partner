"""Habits API endpoints."""

from fastapi import APIRouter, HTTPException
from typing import List
from services.habit_service import (
    create_habit,
    list_habits,
    get_habit_by_id,
    update_habit_name_meta,
    update_habit_category_and_frequency,
    archive_habit,
    unarchive_habit,
    delete_habit_permanently,
    list_archived_habits,
)
from api.schemas import (
    HabitCreate,
    HabitUpdate,
    HabitCategoryFrequencyUpdate,
    HabitResponse,
    CreatedResponse,
    StatusResponse,
)

router = APIRouter()


@router.post("/", response_model=CreatedResponse)
def create_habit_endpoint(habit: HabitCreate):
    """Create a new habit."""
    try:
        habit_id = create_habit(
            habit.name,
            habit.type,
            habit.meta,
            category=habit.category,
            frequency=habit.frequency
        )
        return CreatedResponse(id=habit_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[HabitResponse])
def list_habits_endpoint():
    """List all non-archived habits."""
    return list_habits()


@router.get("/archived", response_model=List[HabitResponse])
def archived_habits_endpoint():
    """List all archived habits."""
    return list_archived_habits()


@router.get("/{habit_id}", response_model=HabitResponse)
def get_habit_endpoint(habit_id: str):
    """Get a specific habit by ID."""
    habit = get_habit_by_id(habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit


@router.put("/{habit_id}", response_model=StatusResponse)
def update_habit_endpoint(habit_id: str, habit: HabitUpdate):
    """Update habit name and metadata."""
    try:
        update_habit_name_meta(habit_id, habit.name, habit.meta)
        return StatusResponse(status="updated")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{habit_id}/settings", response_model=StatusResponse)
def update_habit_settings_endpoint(habit_id: str, settings: HabitCategoryFrequencyUpdate):
    """Update habit category and/or frequency."""
    try:
        update_habit_category_and_frequency(
            habit_id,
            category=settings.category,
            frequency=settings.frequency
        )
        return StatusResponse(status="updated")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{habit_id}", response_model=StatusResponse)
def archive_habit_endpoint(habit_id: str):
    """Archive a habit (soft delete)."""
    archive_habit(habit_id)
    return StatusResponse(status="archived")


@router.put("/{habit_id}/restore", response_model=StatusResponse)
def restore_habit_endpoint(habit_id: str):
    """Restore an archived habit."""
    unarchive_habit(habit_id)
    return StatusResponse(status="restored")


@router.delete("/{habit_id}/permanent", response_model=StatusResponse)
def delete_habit_permanently_endpoint(habit_id: str):
    """Permanently delete a habit and all its entries."""
    delete_habit_permanently(habit_id)
    return StatusResponse(status="deleted")
