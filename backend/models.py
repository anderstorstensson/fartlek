from datetime import date, datetime, timezone

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.db import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)  # Garmin activity id
    name: Mapped[str] = mapped_column(String, default="")
    sport: Mapped[str] = mapped_column(String, index=True)  # e.g. running, trail_running, cycling
    start_time_utc: Mapped[datetime] = mapped_column(DateTime, index=True)
    start_time_local: Mapped[datetime] = mapped_column(DateTime)

    elapsed_s: Mapped[float] = mapped_column(Float, default=0.0)
    moving_s: Mapped[float] = mapped_column(Float, default=0.0)
    distance_m: Mapped[float] = mapped_column(Float, default=0.0)
    avg_hr: Mapped[float | None] = mapped_column(Float, nullable=True)
    max_hr: Mapped[float | None] = mapped_column(Float, nullable=True)
    avg_speed_mps: Mapped[float | None] = mapped_column(Float, nullable=True)
    max_speed_mps: Mapped[float | None] = mapped_column(Float, nullable=True)
    ascent_m: Mapped[float | None] = mapped_column(Float, nullable=True)
    descent_m: Mapped[float | None] = mapped_column(Float, nullable=True)
    calories: Mapped[float | None] = mapped_column(Float, nullable=True)
    avg_cadence: Mapped[float | None] = mapped_column(Float, nullable=True)

    trimp: Mapped[float | None] = mapped_column(Float, nullable=True)
    rtss: Mapped[float | None] = mapped_column(Float, nullable=True)
    hrtss: Mapped[float | None] = mapped_column(Float, nullable=True)

    has_gps: Mapped[bool] = mapped_column(Boolean, default=False)
    has_fit: Mapped[bool] = mapped_column(Boolean, default=False)
    # True when the FIT file shows a structured workout / interval session
    # (workout_step messages or laps with rest intensity).
    is_workout: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)

    laps: Mapped[list["Lap"]] = relationship(
        back_populates="activity", cascade="all, delete-orphan", order_by="Lap.lap_index"
    )
    stream: Mapped["Stream | None"] = relationship(
        back_populates="activity", cascade="all, delete-orphan", uselist=False
    )
    best_efforts: Mapped[list["BestEffort"]] = relationship(
        back_populates="activity", cascade="all, delete-orphan"
    )

    @property
    def is_run(self) -> bool:
        return "running" in (self.sport or "")


class Lap(Base):
    __tablename__ = "laps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    activity_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("activities.id", ondelete="CASCADE"), index=True
    )
    lap_index: Mapped[int] = mapped_column(Integer)
    start_offset_s: Mapped[float] = mapped_column(Float, default=0.0)
    elapsed_s: Mapped[float] = mapped_column(Float, default=0.0)
    distance_m: Mapped[float] = mapped_column(Float, default=0.0)
    avg_hr: Mapped[float | None] = mapped_column(Float, nullable=True)
    max_hr: Mapped[float | None] = mapped_column(Float, nullable=True)
    avg_speed_mps: Mapped[float | None] = mapped_column(Float, nullable=True)
    intensity: Mapped[str | None] = mapped_column(String, nullable=True)  # warmup/active/rest/cooldown

    activity: Mapped[Activity] = relationship(back_populates="laps")


class Stream(Base):
    """Per-activity time series, stored as parallel JSON arrays (downsampled)."""

    __tablename__ = "streams"

    activity_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True
    )
    time_s: Mapped[list] = mapped_column(JSON, default=list)
    distance_m: Mapped[list] = mapped_column(JSON, default=list)
    hr: Mapped[list] = mapped_column(JSON, default=list)
    speed_mps: Mapped[list] = mapped_column(JSON, default=list)
    altitude_m: Mapped[list] = mapped_column(JSON, default=list)
    cadence: Mapped[list] = mapped_column(JSON, default=list)
    lat: Mapped[list] = mapped_column(JSON, default=list)
    lng: Mapped[list] = mapped_column(JSON, default=list)

    activity: Mapped[Activity] = relationship(back_populates="stream")


class BestEffort(Base):
    __tablename__ = "best_efforts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    activity_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("activities.id", ondelete="CASCADE"), index=True
    )
    label: Mapped[str] = mapped_column(String, index=True)  # e.g. "5K"
    distance_m: Mapped[float] = mapped_column(Float)
    duration_s: Mapped[float] = mapped_column(Float)
    start_time_utc: Mapped[datetime] = mapped_column(DateTime, index=True)

    activity: Mapped[Activity] = relationship(back_populates="best_efforts")


class PlannedWorkout(Base):
    """A suggested workout from a training plan (written by the Claude skill)."""

    __tablename__ = "planned_workouts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    day: Mapped[date] = mapped_column(Date, index=True)
    title: Mapped[str] = mapped_column(String)
    workout_type: Mapped[str] = mapped_column(String, default="easy")  # easy/long/intervals/tempo/race/rest/cross
    description: Mapped[str] = mapped_column(String, default="")
    target_distance_m: Mapped[float | None] = mapped_column(Float, nullable=True)
    target_duration_s: Mapped[float | None] = mapped_column(Float, nullable=True)
    plan_name: Mapped[str] = mapped_column(String, default="", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)


class AthleteSettings(Base):
    __tablename__ = "athlete_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    resting_hr: Mapped[int] = mapped_column(Integer, default=55)
    max_hr: Mapped[int] = mapped_column(Integer, default=190)
    lthr: Mapped[int] = mapped_column(Integer, default=170)
    threshold_pace_s_per_km: Mapped[float] = mapped_column(Float, default=270.0)
    sex: Mapped[str] = mapped_column(String, default="male")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, onupdate=_utcnow)


class SyncState(Base):
    __tablename__ = "sync_state"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    status: Mapped[str] = mapped_column(String, default="idle")  # idle | running | error
    message: Mapped[str] = mapped_column(String, default="")
    last_sync_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    synced_activities: Mapped[int] = mapped_column(Integer, default=0)
