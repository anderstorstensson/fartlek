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

    # Running dynamics / power averages (newer watches only; units in the name).
    avg_power_w: Mapped[float | None] = mapped_column(Float, nullable=True)
    avg_vertical_oscillation_mm: Mapped[float | None] = mapped_column(Float, nullable=True)
    avg_vertical_ratio_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    avg_step_length_mm: Mapped[float | None] = mapped_column(Float, nullable=True)
    avg_stance_time_ms: Mapped[float | None] = mapped_column(Float, nullable=True)
    avg_respiration_brpm: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Derived running metrics (runs with usable streams only).
    gap_speed_mps: Mapped[float | None] = mapped_column(Float, nullable=True)
    decoupling_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    # GAP meters per minute per heartbeat: (gap_speed_mps * 60) / avg stream HR.
    efficiency_index: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Weather at activity start (enriched from Open-Meteo; outdoor activities only).
    weather_temp_c: Mapped[float | None] = mapped_column(Float, nullable=True)
    weather_humidity_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    weather_wind_mps: Mapped[float | None] = mapped_column(Float, nullable=True)
    weather_code: Mapped[int | None] = mapped_column(Integer, nullable=True)

    has_gps: Mapped[bool] = mapped_column(Boolean, default=False)
    has_fit: Mapped[bool] = mapped_column(Boolean, default=False)
    # True when the FIT file shows a structured workout / interval session
    # (workout_step messages or laps with rest intensity).
    is_workout: Mapped[bool] = mapped_column(Boolean, default=False)
    # User-set session tag (easy/long/intervals/tempo/race/recovery/cross).
    tag: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    # The athlete's own note ("felt flat, slept 4h", "new shoes") — read by analyses.
    user_note: Mapped[str] = mapped_column(String, default="")
    # True once the user edits the title; auto-naming then leaves it alone.
    name_locked: Mapped[bool] = mapped_column(Boolean, default=False)
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
    # Running dynamics (nullable JSON: rows imported before these existed hold NULL).
    power: Mapped[list | None] = mapped_column(JSON, nullable=True)  # watts
    vertical_oscillation: Mapped[list | None] = mapped_column(JSON, nullable=True)  # mm
    vertical_ratio: Mapped[list | None] = mapped_column(JSON, nullable=True)  # %
    step_length: Mapped[list | None] = mapped_column(JSON, nullable=True)  # mm
    stance_time: Mapped[list | None] = mapped_column(JSON, nullable=True)  # ms
    respiration: Mapped[list | None] = mapped_column(JSON, nullable=True)  # breaths/min

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


class AnalysisNote(Base):
    """A saved analysis written by the Claude skill (session, weekly, trend…).

    activity_id is intentionally NOT a foreign key: re-imports delete and recreate
    activity rows, and notes must survive that.
    """

    __tablename__ = "analysis_notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    activity_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True)
    kind: Mapped[str] = mapped_column(String, default="session", index=True)
    title: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(String)  # markdown
    period_start: Mapped[date | None] = mapped_column(Date, nullable=True)
    period_end: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, onupdate=_utcnow)


class AthleteSettings(Base):
    __tablename__ = "athlete_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    resting_hr: Mapped[int] = mapped_column(Integer, default=55)
    max_hr: Mapped[int] = mapped_column(Integer, default=190)
    lthr: Mapped[int] = mapped_column(Integer, default=170)
    threshold_pace_s_per_km: Mapped[float] = mapped_column(Float, default=270.0)
    sex: Mapped[str] = mapped_column(String, default="male")
    zone_mode: Mapped[str] = mapped_column(String, default="max_hr")  # max_hr | lthr | manual
    manual_zone_bounds: Mapped[list | None] = mapped_column(JSON, nullable=True)  # 5 lower bounds (bpm)
    # rTSS from grade-adjusted pace; disable if the watch's barometric altitude is unreliable.
    rtss_use_gap: Mapped[bool] = mapped_column(Boolean, default=True)
    pace_zone_mode: Mapped[str] = mapped_column(String, default="threshold")  # threshold | manual
    # 5 lower bounds as pace (s/km), slowest first (Z1's slowest pace … Z5's slowest pace).
    manual_pace_zone_bounds: Mapped[list | None] = mapped_column(JSON, nullable=True)
    # How the AI coach talks: drill | harsh | balanced | supportive. Tone only — never substance.
    coaching_tone: Mapped[str] = mapped_column(String, default="balanced")
    # BCP-47 locale for date/time display in the UI; empty = browser default.
    display_locale: Mapped[str] = mapped_column(String, default="")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, onupdate=_utcnow)


class DailyWellness(Base):
    """One row per day of Garmin wellness data (sleep, HRV, RHR, body battery, stress)."""

    __tablename__ = "daily_wellness"

    day: Mapped[date] = mapped_column(Date, primary_key=True)
    resting_hr: Mapped[int | None] = mapped_column(Integer, nullable=True)
    hrv_last_night_avg: Mapped[float | None] = mapped_column(Float, nullable=True)  # ms
    hrv_status: Mapped[str | None] = mapped_column(String, nullable=True)  # BALANCED/LOW/…
    sleep_s: Mapped[float | None] = mapped_column(Float, nullable=True)
    deep_sleep_s: Mapped[float | None] = mapped_column(Float, nullable=True)
    sleep_score: Mapped[int | None] = mapped_column(Integer, nullable=True)  # 0-100
    body_battery_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    body_battery_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    stress_avg: Mapped[int | None] = mapped_column(Integer, nullable=True)
    steps: Mapped[int | None] = mapped_column(Integer, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, onupdate=_utcnow)


class Race(Base):
    """A goal race the athlete is training for."""

    __tablename__ = "races"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    day: Mapped[date] = mapped_column(Date, index=True)
    distance_m: Mapped[float] = mapped_column(Float)
    target_time_s: Mapped[float | None] = mapped_column(Float, nullable=True)
    priority: Mapped[str] = mapped_column(String, default="A")  # A/B/C
    notes: Mapped[str] = mapped_column(String, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)


class CoachMessage(Base):
    """Chat history for the in-app coach (a headless Claude Code session)."""

    __tablename__ = "coach_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    role: Mapped[str] = mapped_column(String)  # user | assistant
    content: Mapped[str] = mapped_column(String)  # markdown
    session_id: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)


class SyncState(Base):
    __tablename__ = "sync_state"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    status: Mapped[str] = mapped_column(String, default="idle")  # idle | running | error
    message: Mapped[str] = mapped_column(String, default="")
    last_sync_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    synced_activities: Mapped[int] = mapped_column(Integer, default=0)
