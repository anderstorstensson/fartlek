"""Race time prediction from recent best efforts (Riegel model).

t2 = t1 * (d2/d1)^1.06. Best efforts are windows inside whatever was run —
workouts included — so each one is a *lower bound* on fitness, never an
overestimate. The prediction therefore uses the fastest extrapolation among
qualifying anchors. Efforts far shorter than the goal distance extrapolate
poorly (a 1K says nothing about a marathon), so only anchors of at least a
fifth of the goal distance qualify.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models import BestEffort

RIEGEL_EXPONENT = 1.06
ANCHOR_WINDOW_DAYS = 120
_MIN_ANCHOR_DISTANCE_M = 1000.0
_MIN_ANCHOR_FRACTION_OF_GOAL = 0.2


@dataclass(frozen=True)
class Prediction:
    time_s: float
    anchor_label: str
    anchor_duration_s: float
    anchor_date: str  # ISO date of the anchor effort


def riegel_time(anchor_distance_m: float, anchor_time_s: float, goal_distance_m: float) -> float:
    return anchor_time_s * (goal_distance_m / anchor_distance_m) ** RIEGEL_EXPONENT


def predict(session: Session, goal_distance_m: float) -> Prediction | None:
    """Fastest Riegel prediction from the best recent effort per qualifying distance."""
    # DB timestamps are naive UTC; compare naive to keep SQLite string ordering sane.
    since = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=ANCHOR_WINDOW_DAYS)
    min_distance = max(_MIN_ANCHOR_DISTANCE_M, goal_distance_m * _MIN_ANCHOR_FRACTION_OF_GOAL)
    efforts = session.scalars(
        select(BestEffort)
        .where(BestEffort.start_time_utc >= since)
        .where(BestEffort.distance_m >= min_distance)
    ).all()

    fastest_per_label: dict[str, BestEffort] = {}
    for effort in efforts:
        best = fastest_per_label.get(effort.label)
        if best is None or effort.duration_s < best.duration_s:
            fastest_per_label[effort.label] = effort

    best_prediction: Prediction | None = None
    for effort in fastest_per_label.values():
        if not effort.distance_m or not effort.duration_s:
            continue
        time_s = riegel_time(effort.distance_m, effort.duration_s, goal_distance_m)
        if best_prediction is None or time_s < best_prediction.time_s:
            best_prediction = Prediction(
                time_s=time_s,
                anchor_label=effort.label,
                anchor_duration_s=effort.duration_s,
                anchor_date=effort.start_time_utc.date().isoformat(),
            )
    return best_prediction


def predict_time_s(session: Session, goal_distance_m: float) -> float | None:
    prediction = predict(session, goal_distance_m)
    return prediction.time_s if prediction else None
