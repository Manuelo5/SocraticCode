"""Four-step scripted hint progression for guided exercises."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Callable

from ai_tutor import TutorHint, generate_hint as generate_ai_hint
from exercises import Exercise

MAX_HINT_LEVEL = 4


def get_next_hint(exercise: Exercise, hints_used: int) -> tuple[int, str] | None:
    """Return one next hint, or None when hints are disabled or exhausted."""
    if exercise.is_solo_check or hints_used < 0 or hints_used >= MAX_HINT_LEVEL:
        return None
    return hints_used + 1, exercise.hints[hints_used]


def request_next_hint(
    exercise: Exercise,
    student_code: str,
    hints_used: int,
    previous_hints: Sequence[str],
    *,
    api_key: str | None,
    model: str,
    generate: Callable[..., TutorHint] | None = None,
) -> TutorHint | None:
    """Request only the next allowed level; the Solo Check never reaches the AI."""
    next_hint = get_next_hint(exercise, hints_used)
    if next_hint is None:
        return None
    level, _ = next_hint
    generator = generate or generate_ai_hint
    return generator(
        exercise,
        student_code,
        level,
        previous_hints,
        api_key=api_key,
        model=model,
    )
