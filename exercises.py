"""Definitions for the three beginner debugging exercises."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Exercise:
    id: str
    function_name: str
    title: str
    description: str
    learning_objective: str
    starter_code: str
    expected_behaviour: str
    reference_solution: str
    hints: tuple[str, str, str, str]
    is_solo_check: bool = False


EXERCISES = (
    Exercise(
        id="average",
        function_name="calculate_average",
        title="Exercise 1: Calculate an average",
        description=(
            "This function should calculate the arithmetic average of a non-empty "
            "list of numbers, but its result is not always accurate."
        ),
        learning_objective=(
            "Understand how division operators affect numeric results when calculating "
            "a mean."
        ),
        starter_code="""def calculate_average(numbers):
    return sum(numbers) // len(numbers)
""",
        expected_behaviour=(
            "For example, calculate_average([2, 3]) should return 2.5. "
            "Assume the list contains at least one number."
        ),
        reference_solution="""def calculate_average(numbers):
    return sum(numbers) / len(numbers)
""",
        hints=(
            "An average is a total shared equally across a count. Think about whether the result may need to keep a fractional part.",
            "Look at the division operator in the return statement.",
            "The calculation should use division that preserves a fractional result, rather than rounding down to a whole number.",
            "A partial pattern is `sum(numbers) / ...`; decide what should replace the dots to represent the number of items.",
        ),
    ),
    Exercise(
        id="even",
        function_name="is_even",
        title="Exercise 2: Check whether a number is even",
        description=(
            "This function should return True for even integers and False for odd "
            "integers. Inspect how the remainder is used."
        ),
        learning_objective=(
            "Use the modulo operator and a comparison to reason about divisibility."
        ),
        starter_code="""def is_even(number):
    return number % 2 == 1
""",
        expected_behaviour=(
            "For example, is_even(4) should return True and is_even(5) should return False."
        ),
        reference_solution="""def is_even(number):
    return number % 2 == 0
""",
        hints=(
            "The remainder after division can tell you whether an integer is divisible by another number.",
            "Focus on the comparison at the end of the return statement.",
            "An even integer has no remainder after division by two.",
            "`number % 2 == ...` is the comparison shape; choose the value that means there is no remainder.",
        ),
    ),
    Exercise(
        id="larger",
        function_name="larger_of_two",
        title="Solo Check: Return the larger number",
        description=(
            "Independently fix this function so that it returns whichever of its two "
            "inputs is larger. No hints are available for this challenge."
        ),
        learning_objective=(
            "Independently reason about conditional comparisons and returned values."
        ),
        starter_code="""def larger_of_two(first, second):
    if first < second:
        return first
    return second
""",
        expected_behaviour=(
            "For example, larger_of_two(8, 3) should return 8 and larger_of_two(2, 6) should return 6."
        ),
        reference_solution="""def larger_of_two(first, second):
    if first > second:
        return first
    return second
""",
        hints=(
            "A comparison can tell you which input has the greater value.",
            "Focus on the condition that chooses which input to return.",
            "The function should return the first input only when it is greater than the second.",
            "`if first > ...:` is a useful comparison shape; decide which input belongs after `>`.",
        ),
        is_solo_check=True,
    ),
)

EXERCISES_BY_ID = {exercise.id: exercise for exercise in EXERCISES}
