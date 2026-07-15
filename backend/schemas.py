from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class ActivitySummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    sport: str
    start_time_local: datetime
    elapsed_s: float
    moving_s: float
    distance_m: float
    avg_hr: float | None
    max_hr: float | None
    avg_speed_mps: float | None
    ascent_m: float | None
    trimp: float | None
    rtss: float | None
    hrtss: float | None
    has_gps: bool
    is_workout: bool


class LapOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    lap_index: int
    start_offset_s: float
    elapsed_s: float
    distance_m: float
    avg_hr: float | None
    max_hr: float | None
    avg_speed_mps: float | None
    intensity: str | None


class BestEffortOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    label: str
    distance_m: float
    duration_s: float


class ActivityDetail(ActivitySummary):
    max_speed_mps: float | None
    descent_m: float | None
    calories: float | None
    avg_cadence: float | None
    has_fit: bool
    laps: list[LapOut]
    best_efforts: list[BestEffortOut]


class ActivityList(BaseModel):
    items: list[ActivitySummary]
    total: int


class ZoneOut(BaseModel):
    name: str
    low_bpm: int
    high_bpm: int | None


class StreamsOut(BaseModel):
    time_s: list[float | None]
    distance_m: list[float | None]
    hr: list[float | None]
    speed_mps: list[float | None]
    altitude_m: list[float | None]
    cadence: list[float | None]
    lat: list[float | None]
    lng: list[float | None]
    zones: list[ZoneOut]
    time_in_zones_s: list[float]


class FitnessPoint(BaseModel):
    day: date
    load: float
    ctl: float
    atl: float
    tsb: float


class WeeklyStat(BaseModel):
    week_start: date
    run_distance_m: float
    total_moving_s: float
    load_trimp: float
    load_rtss: float
    activities: int
    runs: int
    ascent_m: float


class LogbookActivity(BaseModel):
    id: int
    name: str
    sport: str
    day_index: int  # 0 = Monday … 6 = Sunday
    distance_m: float
    moving_s: float
    start_time_local: datetime
    is_workout: bool


class LogbookWeek(BaseModel):
    week_start: date
    run_distance_m: float = 0.0
    total_moving_s: float = 0.0
    runs: int = 0
    activities: list[LogbookActivity] = []


class PlannedWorkoutIn(BaseModel):
    day: date
    title: str = Field(min_length=1, max_length=200)
    workout_type: str = Field(
        default="easy", pattern="^(easy|long|intervals|tempo|race|rest|cross)$"
    )
    description: str = ""
    target_distance_m: float | None = Field(default=None, ge=0)
    target_duration_s: float | None = Field(default=None, ge=0)
    plan_name: str = ""


class PlannedWorkoutOut(PlannedWorkoutIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    completed_activity_id: int | None = None


class PlanImport(BaseModel):
    workouts: list[PlannedWorkoutIn] = Field(min_length=1, max_length=500)
    replace_plan: bool = False  # delete existing workouts with the same plan_name first


class PlanInfo(BaseModel):
    plan_name: str
    workouts: int
    first_day: date
    last_day: date


class RecordEntry(BaseModel):
    label: str
    distance_m: float
    duration_s: float
    activity_id: int
    activity_name: str
    start_time_local: datetime


class WeekSummary(BaseModel):
    run_distance_m: float = 0.0
    total_moving_s: float = 0.0
    load_trimp: float = 0.0
    activities: int = 0
    runs: int = 0


class FormSnapshot(BaseModel):
    ctl: float
    atl: float
    tsb: float


class StatsSummary(BaseModel):
    this_week: WeekSummary
    last_week: WeekSummary
    form_trimp: FormSnapshot
    form_rtss: FormSnapshot
    total_activities: int


class SettingsOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    resting_hr: int
    max_hr: int
    lthr: int
    threshold_pace_s_per_km: float
    sex: str


class SettingsIn(BaseModel):
    resting_hr: int = Field(ge=25, le=120)
    max_hr: int = Field(ge=120, le=230)
    lthr: int = Field(ge=100, le=220)
    threshold_pace_s_per_km: float = Field(ge=120, le=720)
    sex: str = Field(pattern="^(male|female)$")


class SettingsResponse(SettingsOut):
    zones: list[ZoneOut]


class SyncStatus(BaseModel):
    status: str
    message: str
    last_sync_at: datetime | None
    logged_in: bool
    total_activities: int
