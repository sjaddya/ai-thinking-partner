"""Pydantic schemas for API request/response models."""

from pydantic import BaseModel
from typing import Optional, Dict, List, Union


# ========== REQUEST MODELS ==========

class HabitCreate(BaseModel):
    name: str
    type: str
    meta: Dict = {}
    category: str = "General"
    frequency: str = "daily"


class HabitUpdate(BaseModel):
    name: str
    meta: Dict


class HabitCategoryFrequencyUpdate(BaseModel):
    category: Optional[str] = None
    frequency: Optional[str] = None


class EntryCreate(BaseModel):
    habit_id: str
    date: str
    value: int | str | None = None


class TimerSession(BaseModel):
    habit_id: str
    date: str
    seconds: int


# ========== RESPONSE MODELS ==========

class HabitResponse(BaseModel):
    id: str
    name: str
    type: str
    meta: Dict
    category: str
    frequency: str


class CreatedResponse(BaseModel):
    id: str


class StatusResponse(BaseModel):
    status: str


class EntryDetailResponse(BaseModel):
    habit_id: str
    name: str
    type: str
    complete: bool
    value: Optional[str] = None


class ProgressResponse(BaseModel):
    date: str
    total: int
    completed: int
    percentage: float
    details: List[EntryDetailResponse]


class MonthlyDayResponse(BaseModel):
    date: str
    completed: int
    total: int


class MonthlyResponse(BaseModel):
    year: int
    month: int
    days: List[MonthlyDayResponse]


class StreakResponse(BaseModel):
    habit_id: str
    current_streak: Optional[int] = None
    longest_streak: Optional[int] = None


class AnalyticsResponse(BaseModel):
    total: float
    average: Optional[float] = None
    days_logged: int
    unit: Optional[str] = None
    completion_rate: Optional[float] = None
    scale_min: Optional[int] = None
    scale_max: Optional[int] = None
    minutes_total: Optional[float] = None
