from exercises import EXERCISES


def test_three_exercises_have_required_topics_and_solo_check() -> None:
    assert len(EXERCISES) == 3
    assert [exercise.id for exercise in EXERCISES] == ["average", "even", "larger"]
    assert [exercise.is_solo_check for exercise in EXERCISES] == [False, False, True]


def test_each_exercise_has_four_hints_and_starter_and_reference_code() -> None:
    for exercise in EXERCISES:
        assert len(exercise.hints) == 4
        assert exercise.starter_code
        assert exercise.reference_solution
        assert exercise.function_name in exercise.starter_code
        assert all(exercise.reference_solution not in hint for hint in exercise.hints)
