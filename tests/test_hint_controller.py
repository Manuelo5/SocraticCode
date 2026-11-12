from exercises import EXERCISES
from hint_controller import MAX_HINT_LEVEL, get_next_hint
from ai_tutor import TutorHint
from hint_controller import request_next_hint


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


def test_request_next_hint_calls_generator_for_only_the_next_level() -> None:
    exercise = EXERCISES[0]
    captured: dict[str, object] = {}

    def fake_generate(
        selected_exercise,
        student_code,
        hint_level,
        previous_hints,
        *,
        api_key,
        model,
    ) -> TutorHint:
        captured.update(
            exercise=selected_exercise,
            student_code=student_code,
            hint_level=hint_level,
            previous_hints=previous_hints,
            api_key=api_key,
            model=model,
        )
        return TutorHint(hint_level, "A mock hint", "ai")

    hint = request_next_hint(
        exercise,
        "student code",
        2,
        ["level one", "level two"],
        api_key="test-key",
        model="test-model",
        generate=fake_generate,
    )

    assert hint == TutorHint(3, "A mock hint", "ai")
    assert captured["hint_level"] == 3
    assert captured["student_code"] == "student code"


def test_solo_check_request_never_calls_ai_generator() -> None:
    called = False

    def unexpected_generate(*args, **kwargs) -> TutorHint:
        nonlocal called
        called = True
        raise AssertionError("The Solo Check must not call the AI tutor.")

    result = request_next_hint(
        EXERCISES[2],
        EXERCISES[2].starter_code,
        0,
        [],
        api_key="test-key",
        model="test-model",
        generate=unexpected_generate,
    )

    assert result is None
    assert not called
