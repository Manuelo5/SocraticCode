from exercises import EXERCISES
from hint_controller import MAX_HINT_LEVEL
from progress_tracker import (
    can_access_exercise,
    create_progress,
    record_hint,
    record_submission,
    save_draft,
)


def test_exercises_unlock_in_sequence_and_solo_requires_both_guided_tasks() -> None:
    progress = create_progress()
    assert can_access_exercise(0, progress)
    assert not can_access_exercise(1, progress)
    assert not can_access_exercise(2, progress)

    record_submission(progress, EXERCISES[0], passed=True)
    assert can_access_exercise(1, progress)
    assert not can_access_exercise(2, progress)

    record_submission(progress, EXERCISES[1], passed=True)
    assert can_access_exercise(2, progress)


def test_solo_check_cannot_consume_hints_and_tracks_outcome() -> None:
    progress = create_progress()
    solo_check = EXERCISES[2]

    assert not record_hint(progress, solo_check)
    assert progress["hints_by_exercise"]["larger"] == 0

    record_submission(progress, solo_check, passed=False)
    assert progress["solo_check_passed"] is False
    record_submission(progress, solo_check, passed=True)
    assert progress["solo_check_passed"] is True
    assert progress["submissions_by_exercise"]["larger"] == 2


def test_hint_usage_increments_individually_and_stops_at_maximum() -> None:
    progress = create_progress()
    guided_exercise = EXERCISES[0]

    for expected_count in range(1, MAX_HINT_LEVEL + 1):
        assert record_hint(progress, guided_exercise)
        assert progress["hints_by_exercise"]["average"] == expected_count

    assert not record_hint(progress, guided_exercise)
    assert progress["hints_by_exercise"]["average"] == MAX_HINT_LEVEL


def test_student_draft_is_retained_when_session_progress_changes() -> None:
    progress = create_progress()
    draft = "def calculate_average(numbers):\n    return sum(numbers) / len(numbers)\n"

    save_draft(progress, "average", draft)
    record_hint(progress, EXERCISES[0])

    assert progress["drafts"]["average"] == draft
