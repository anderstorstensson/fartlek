import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.api import (
    activities,
    coach,
    notes,
    plan,
    races,
    settings,
    sync,
    trends,
    wellness,
)
from backend.config import BASE_DIR, config
from backend.db import init_db
from backend.sync.scheduler import start_scheduler, stop_scheduler

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")

FRONTEND_DIST = BASE_DIR / "frontend" / "dist"


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    if config.scheduler_enabled:
        start_scheduler()
    yield
    stop_scheduler()


app = FastAPI(title="Fartlek", lifespan=lifespan)

app.include_router(activities.router)
app.include_router(notes.router)
app.include_router(plan.router)
app.include_router(trends.router)
app.include_router(settings.router)
app.include_router(sync.router)
app.include_router(wellness.router)
app.include_router(races.router)
app.include_router(coach.router)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


def _mount_frontend(app: FastAPI, dist: Path) -> None:
    if not dist.exists():
        return
    app.mount("/assets", StaticFiles(directory=dist / "assets"), name="assets")

    @app.get("/{path:path}", include_in_schema=False)
    def spa(path: str) -> FileResponse:
        candidate = dist / path
        if path and candidate.is_file() and candidate.resolve().is_relative_to(dist.resolve()):
            return FileResponse(candidate)
        return FileResponse(dist / "index.html")


_mount_frontend(app, FRONTEND_DIST)
