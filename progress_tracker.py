"""Small helpers for session-only exercise, hint, and submission progress."""

from __future__ import annotations

from typing import Any

from exercises import EXERCISES, Exercise
from hint_controller import MAX_HINT_LEVEL


def create_progress() -> dict[str, Any]:
    return {
        "completed_exercises": [],
        "hints_by_exercise": {exercise.id: 0 for exercise in EXERCISES},
        "submissions_by_exercise": {exercise.id: 0 for exercise in EXERCISES},
        "drafts": {exercise.id: exercise.starter_code for exercise in EXERCISES},
        "hint_history": {exercise.id: [] for exercise in EXERCISES},
        "hint_cache": {exercise.id: {} for exercise in EXERCISES},
        "solo_check_passed": False,
    }


def save_draft(progress: dict[str, Any], exercise_id: str, code: str) -> None:
    progress["drafts"][exercise_id] = code


def record_hint(progress: dict[str, Any], exercise: Exercise) -> bool:
    if (
        exercise.is_solo_check
        or progress["hints_by_exercise"][exercise.id] >= MAX_HINT_LEVEL
    ):
        return False
    progress["hints_by_exercise"][exercise.id] += 1
    return True


def record_submission(progress: dict[str, Any], exercise: Exercise, passed: bool) -> None:
    progress["submissions_by_exercise"][exercise.id] += 1
    if passed and exercise.id not in progress["completed_exercises"]:
        progress["completed_exercises"].append(exercise.id)
    if exercise.is_solo_check:
        progress["solo_check_passed"] = passed


def can_access_exercise(index: int, progress: dict[str, Any]) -> bool:
    if index == 0:
        return True
    if index == 1:
        return "average" in progress["completed_exercises"]
    if index == 2:
        return all(
            exercise_id in progress["completed_exercises"]
            for exercise_id in ("average", "even")
        )
    return False
