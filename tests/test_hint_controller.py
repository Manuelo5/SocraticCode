from exercises import EXERCISES
from hint_controller import MAX_HINT_LEVEL, get_next_hint


def test_hints_advance_one_level_and_stop_after_four() -> None:
    exercise = EXERCISES[0]
    assert get_next_hint(exercise, 0) == (1, exercise.hints[0])
    assert get_next_hint(exercise, 1) == (2, exercise.hints[1])
    assert get_next_hint(exercise, 2) == (3, exercise.hints[2])
    assert get_next_hint(exercise, 3) == (4, exercise.hints[3])
    assert get_next_hint(exercise, MAX_HINT_LEVEL) is None


def test_solo_check_has_no_hints() -> None:
    solo_check = EXERCISES[2]
    assert solo_check.is_solo_check
    assert get_next_hint(solo_check, 0) is None
