from exercises import EXERCISES
from evaluator import evaluate_submission


def test_reference_solutions_are_accepted() -> None:
    for exercise in EXERCISES:
        result = evaluate_submission(exercise, exercise.reference_solution)
        assert result.status == "correct"
        assert "supported solution pattern" in result.message


def test_buggy_starters_are_incorrect() -> None:
    for exercise in EXERCISES:
        assert evaluate_submission(exercise, exercise.starter_code).status == "incorrect"


def test_average_with_simple_local_aliases_is_accepted() -> None:
    alternative = """def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)
    return total / count
"""
    assert evaluate_submission(EXERCISES[0], alternative).status == "correct"


def test_average_using_floor_division_is_incorrect() -> None:
    incorrect = """def calculate_average(numbers):
    return sum(numbers) // len(numbers)
"""
    result = evaluate_submission(EXERCISES[0], incorrect)
    assert result.status == "incorrect"
    assert "expected behavior" in result.message


def test_average_does_not_accept_rebound_builtin_aliases() -> None:
    shadowed = """def calculate_average(numbers):
    sum = len
    count = len(numbers)
    return sum(numbers) / count
"""
    assert evaluate_submission(EXERCISES[0], shadowed).status == "unsupported"


def test_even_check_accepts_equivalent_remainder_patterns() -> None:
    alternatives = (
        """def is_even(number):
    return number % 2 != 1
""",
        """def is_even(number):
    return not (number % 2)
""",
        """def is_even(number):
    return 0 == number % 2
""",
    )
    for alternative in alternatives:
        assert evaluate_submission(EXERCISES[1], alternative).status == "correct"


def test_even_check_rejects_odd_predicate() -> None:
    incorrect = """def is_even(number):
    return number % 2 == 1
"""
    assert evaluate_submission(EXERCISES[1], incorrect).status == "incorrect"


def test_solo_check_accepts_explicit_else_branch() -> None:
    alternative = """def larger_of_two(first, second):
    if first > second:
        return first
    else:
        return second
"""
    assert evaluate_submission(EXERCISES[2], alternative).status == "correct"


def test_solo_check_accepts_equivalent_conditional_expression_and_max_call() -> None:
    alternatives = (
        """def larger_of_two(first, second):
    return first if first >= second else second
""",
        """def larger_of_two(first, second):
    return max(first, second)
""",
    )
    for alternative in alternatives:
        assert evaluate_submission(EXERCISES[2], alternative).status == "correct"


def test_solo_check_rejects_function_that_returns_the_smaller_number() -> None:
    smaller = """def larger_of_two(first, second):
    if first > second:
        return second
    else:
        return first
"""
    assert evaluate_submission(EXERCISES[2], smaller).status == "incorrect"


def test_syntax_error_gets_distinct_feedback() -> None:
    result = evaluate_submission(
        EXERCISES[0], "def calculate_average(numbers)\n    return 0\n"
    )
    assert result.status == "syntax_error"
    assert "line 1" in result.message
    assert "syntax" in result.message


def test_valid_but_unsupported_structure_is_not_called_incorrect() -> None:
    unsupported = """def calculate_average(numbers):
    return sum(numbers) / len(numbers) + 0
"""
    result = evaluate_submission(EXERCISES[0], unsupported)
    assert result.status == "unsupported"
    assert "cannot verify safely" in result.message


def test_untrusted_submission_is_parsed_but_never_executed(tmp_path) -> None:
    marker = tmp_path / "should_not_exist"
    source = f"""def calculate_average(numbers):
    open({str(marker)!r}, "w").write("executed")
    return sum(numbers) / len(numbers)
"""
    result = evaluate_submission(EXERCISES[0], source)
    assert result.status == "unsupported"
    assert not marker.exists()
