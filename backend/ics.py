"""Minimal iCalendar (RFC 5545) generation for planned workouts."""

from datetime import datetime, timedelta, timezone

from backend.models import PlannedWorkout
from backend.plan_export import description_text, stable_keys


def _escape(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\r\n", "\\n")
        .replace("\n", "\\n")
    )


def _fold(line: str) -> list[str]:
    """RFC 5545 line folding: max 75 octets, continuations start with a space."""
    encoded = line.encode("utf-8")
    if len(encoded) <= 75:
        return [line]
    parts: list[str] = []
    current = b""
    for char in line:
        char_bytes = char.encode("utf-8")
        limit = 75 if not parts else 74  # continuation lines lose one octet to the space
        if len(current) + len(char_bytes) > limit:
            parts.append(current.decode("utf-8"))
            current = char_bytes
        else:
            current += char_bytes
    if current:
        parts.append(current.decode("utf-8"))
    return [parts[0]] + [" " + p for p in parts[1:]]


def plan_to_ics(workouts: list[PlannedWorkout], calendar_name: str = "Fartlek plan") -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines: list[str] = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Fartlek//training plan//EN",
        "CALSCALE:GREGORIAN",
        f"X-WR-CALNAME:{_escape(calendar_name)}",
    ]
    keys = stable_keys(workouts)
    for workout in workouts:
        start = workout.day.strftime("%Y%m%d")
        end = (workout.day + timedelta(days=1)).strftime("%Y%m%d")
        lines.extend(
            [
                "BEGIN:VEVENT",
                f"UID:fartlek-{keys[workout.id]}@fartlek.local",
                f"DTSTAMP:{stamp}",
                f"DTSTART;VALUE=DATE:{start}",
                f"DTEND;VALUE=DATE:{end}",
                f"SUMMARY:{_escape(workout.title)}",
                f"DESCRIPTION:{_escape(description_text(workout))}",
                f"CATEGORIES:{_escape(workout.workout_type.upper())}",
                "TRANSP:TRANSPARENT",
                "END:VEVENT",
            ]
        )
    lines.append("END:VCALENDAR")
    folded: list[str] = []
    for line in lines:
        folded.extend(_fold(line))
    return "\r\n".join(folded) + "\r\n"
