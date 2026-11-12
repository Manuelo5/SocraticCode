from exercises import EXERCISES
from evaluator import evaluate_submission


def test_reference_solutions_are_accepted() -> None:
    for exercise in EXERCISES:
        assert evaluate_submission(exercise, exercise.reference_solution).status == "correct"


def test_buggy_starters_are_incorrect() -> None:
    for exercise in EXERCISES:
        assert evaluate_submission(exercise, exercise.starter_code).status == "incorrect"


def test_syntax_error_gets_distinct_feedback() -> None:
    result = evaluate_submission(EXERCISES[0], "def calculate_average(numbers)\n    return 0\n")
    assert result.status == "syntax_error"
    assert "parse" in result.message


def test_alternative_correct_implementation_may_not_match_structure() -> None:
    alternative = """def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)
    return total / count
"""
    assert evaluate_submission(EXERCISES[0], alternative).status == "incorrect"


def test_submission_with_extra_executable_statements_is_not_run(tmp_path) -> None:
    marker = tmp_path / "should_not_exist"
    source = (
        f"open({str(marker)!r}, 'w').write('executed')\n"
        + EXERCISES[0].reference_solution
    )
    result = evaluate_submission(EXERCISES[0], source)
    assert result.status == "incorrect"
    assert not marker.exists()
