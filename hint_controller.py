"""Four-step scripted hint progression for guided exercises."""

from __future__ import annotations

from exercises import Exercise

MAX_HINT_LEVEL = 4


def get_next_hint(exercise: Exercise, hints_used: int) -> tuple[int, str] | None:
    """Return one next hint, or None when hints are disabled or exhausted."""
    if exercise.is_solo_check or hints_used < 0 or hints_used >= MAX_HINT_LEVEL:
        return None
    return hints_used + 1, exercise.hints[hints_used]
