from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


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
    tag: str | None = None


class ActivityUpdate(BaseModel):
    """PATCH payload — only provided fields change. Empty tag clears it."""

    name: str | None = Field(default=None, min_length=1, max_length=200)
    tag: str | None = Field(
        default=None, pattern="^(easy|recovery|long|intervals|tempo|race|cross|)$"
    )
    user_note: str | None = Field(default=None, max_length=10000)


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
    avg_power_w: float | None = None
    avg_vertical_oscillation_mm: float | None = None
    avg_vertical_ratio_pct: float | None = None
    avg_step_length_mm: float | None = None
    avg_stance_time_ms: float | None = None
    avg_respiration_brpm: float | None = None
    gap_speed_mps: float | None = None
    decoupling_pct: float | None = None
    efficiency_index: float | None = None
    weather_temp_c: float | None = None
    weather_humidity_pct: float | None = None
    weather_wind_mps: float | None = None
    weather_code: int | None = None
    user_note: str = ""
    laps: list[LapOut]
    best_efforts: list[BestEffortOut]


class ActivityList(BaseModel):
    items: list[ActivitySummary]
    total: int


class ZoneOut(BaseModel):
    name: str
    low_bpm: int
    high_bpm: int | None


class PaceZoneOut(BaseModel):
    name: str
    low_speed_mps: float
    high_speed_mps: float | None


class StreamsOut(BaseModel):
    time_s: list[float | None]
    distance_m: list[float | None]
    hr: list[float | None]
    speed_mps: list[float | None]
    gap_speed_mps: list[float | None] = []  # derived server-side, not stored
    altitude_m: list[float | None]
    cadence: list[float | None]
    lat: list[float | None]
    lng: list[float | None]
    power: list[float | None] = []
    vertical_oscillation: list[float | None] = []
    vertical_ratio: list[float | None] = []
    step_length: list[float | None] = []
    stance_time: list[float | None] = []
    respiration: list[float | None] = []
    zones: list[ZoneOut]
    time_in_zones_s: list[float]
    pace_zones: list[PaceZoneOut] = []
    time_in_pace_zones_s: list[float] = []


class FitnessPoint(BaseModel):
    day: date
    load: float
    ctl: float
    atl: float
    tsb: float
    projected: bool = False


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


class NoteIn(BaseModel):
    activity_id: int | None = None
    kind: str = Field(
        default="session", pattern="^(session|race|weekly|trend|plan-checkin|other)$"
    )
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=50000)
    period_start: date | None = None
    period_end: date | None = None


class NoteOut(NoteIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


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
    zone_mode: str
    manual_zone_bounds: list[int] | None
    rtss_use_gap: bool
    pace_zone_mode: str
    manual_pace_zone_bounds: list[float] | None
    coaching_tone: str


class SettingsIn(BaseModel):
    resting_hr: int = Field(ge=25, le=120)
    max_hr: int = Field(ge=120, le=230)
    lthr: int = Field(ge=100, le=220)
    threshold_pace_s_per_km: float = Field(ge=120, le=720)
    sex: str = Field(pattern="^(male|female)$")
    zone_mode: str = Field(default="max_hr", pattern="^(max_hr|lthr|manual)$")
    manual_zone_bounds: list[int] | None = None
    rtss_use_gap: bool = True
    pace_zone_mode: str = Field(default="threshold", pattern="^(threshold|manual)$")
    manual_pace_zone_bounds: list[float] | None = None
    coaching_tone: str = Field(default="balanced", pattern="^(harsh|balanced|supportive)$")

    @model_validator(mode="after")
    def _check_manual_bounds(self) -> "SettingsIn":
        if self.zone_mode == "manual":
            bounds = self.manual_zone_bounds
            if bounds is None or len(bounds) != 5:
                raise ValueError("manual zone mode requires 5 lower bounds (bpm)")
            if any(b2 <= b1 for b1, b2 in zip(bounds, bounds[1:])):
                raise ValueError("manual zone bounds must be strictly increasing")
            if bounds[0] < 40 or bounds[-1] > 230:
                raise ValueError("manual zone bounds must be plausible bpm values")
        if self.pace_zone_mode == "manual":
            paces = self.manual_pace_zone_bounds
            if paces is None or len(paces) != 5:
                raise ValueError("manual pace zones require 5 lower bounds (s/km, slowest first)")
            if any(p2 >= p1 for p1, p2 in zip(paces, paces[1:])):
                raise ValueError("manual pace bounds must get strictly faster (decreasing s/km)")
            if paces[0] > 1200 or paces[-1] < 120:
                raise ValueError("manual pace bounds must be plausible paces (s/km)")
        return self


class SettingsResponse(SettingsOut):
    zones: list[ZoneOut]
    pace_zones: list["PaceZoneOut"] = []


class SyncStatus(BaseModel):
    status: str
    message: str
    last_sync_at: datetime | None
    logged_in: bool
    total_activities: int


class WeeklyZones(BaseModel):
    week_start: date
    zone_seconds: list[float]  # Z1..Z5
    total_s: float


class EfficiencyPoint(BaseModel):
    day: date
    activity_id: int
    name: str
    efficiency_index: float | None
    decoupling_pct: float | None
    distance_m: float
    moving_s: float
    is_workout: bool


class WellnessDay(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    day: date
    resting_hr: int | None
    hrv_last_night_avg: float | None
    hrv_status: str | None
    sleep_s: float | None
    deep_sleep_s: float | None
    sleep_score: int | None
    body_battery_max: int | None
    body_battery_min: int | None
    stress_avg: int | None
    steps: int | None


class ReadinessOut(BaseModel):
    day: date
    resting_hr: int | None
    resting_hr_baseline: float | None
    hrv_last_night_avg: float | None
    hrv_baseline: float | None
    sleep_score: int | None
    sleep_s: float | None
    body_battery_max: int | None
    stress_avg: int | None
    flags: list[str]
    status: str  # ready | caution | rest


class RaceIn(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    day: date
    distance_m: float = Field(gt=0)
    target_time_s: float | None = Field(default=None, gt=0)
    priority: str = Field(default="A", pattern="^[ABC]$")
    notes: str = ""


class CoachMessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: str
    content: str
    created_at: datetime


class CoachMessageIn(BaseModel):
    text: str = Field(min_length=1, max_length=8000)


class RaceOut(RaceIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    days_until: int | None = None
    predicted_time_s: float | None = None
    # Which best effort the prediction extrapolates from, e.g.
    # "Half marathon 1:23:08 (2026-06-28)" — so the athlete can judge the anchor.
    predicted_from: str | None = None
