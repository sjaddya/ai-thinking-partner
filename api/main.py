"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from api.routers import habits, entries, progress, streaks, monthly, analytics

app = FastAPI(title="AI Thinking Partner API")

app.include_router(habits.router, prefix="/habits", tags=["Habits"])
app.include_router(entries.router, prefix="/entries", tags=["Entries"])
app.include_router(progress.router, prefix="/progress", tags=["Progress"])
app.include_router(streaks.router, prefix="/streaks", tags=["Streaks"])
app.include_router(monthly.router, prefix="/monthly", tags=["Monthly"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def serve_home():
    return FileResponse("static/index.html")
