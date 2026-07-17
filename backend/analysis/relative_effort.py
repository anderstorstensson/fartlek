"""Relative effort: one session's training load in the context of recent training.

Same idea as Strava's Relative Effort — the session's HR-based load (TRIMP)
ranked against every loaded session in the trailing window, expressed as a
midrank percentile plus a qualitative band. Pure computation; the API layer
supplies the loads.
"""

WINDOW_DAYS = 90
MIN_SESSIONS = 5  # below this the percentile is meaningless noise

# Percentile upper bounds → band name; above the last bound = "massive".
_BANDS = ((40.0, "easy"), (70.0, "moderate"), (90.0, "tough"))


def effort_percentile(load: float, recent_loads: list[float]) -> float | None:
    """Midrank percentile of `load` among `recent_loads` (0–100), or None when
    there is too little history to rank against."""
    if len(recent_loads) < MIN_SESSIONS:
        return None
    below = sum(1 for other in recent_loads if other < load)
    ties = sum(1 for other in recent_loads if other == load)
    return round(100.0 * (below + 0.5 * ties) / len(recent_loads), 1)


def effort_band(percentile: float | None) -> str | None:
    if percentile is None:
        return None
    for upper, name in _BANDS:
        if percentile < upper:
            return name
    return "massive"
