"""Safe, deterministic structural checking without executing submitted code."""

from __future__ import annotations

import ast
from dataclasses import dataclass

from exercises import Exercise


@dataclass(frozen=True)
class EvaluationResult:
    status: str
    message: str


def _target_function(source: str, function_name: str) -> ast.FunctionDef | ast.AsyncFunctionDef | None:
    """Parse a function-only submission and find its synchronous target function."""
    tree = ast.parse(source)
    matches = [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == function_name
    ]
    if (
        len(tree.body) != 1
        or len(matches) != 1
        or isinstance(matches[0], ast.AsyncFunctionDef)
    ):
        return None
    return matches[0]


def evaluate_submission(exercise: Exercise, source: str) -> EvaluationResult:
    """Check the target function's AST against its reference; never execute source."""
    try:
        submitted = _target_function(source, exercise.function_name)
        reference = _target_function(exercise.reference_solution, exercise.function_name)
    except SyntaxError as exc:
        line = f" on line {exc.lineno}" if exc.lineno is not None else ""
        return EvaluationResult("syntax_error", f"Python could not parse your code{line}.")

    if submitted is None:
        return EvaluationResult(
            "incorrect",
            f"Submit only one regular function named `{exercise.function_name}` and check its structure.",
        )
    if reference is None:
        raise ValueError(f"Exercise {exercise.id!r} has an invalid reference function.")

    if ast.dump(submitted, include_attributes=False) == ast.dump(
        reference, include_attributes=False
    ):
        return EvaluationResult(
            "correct",
            "Your function matches the expected structure. You can move on to the next exercise.",
        )
    return EvaluationResult(
        "incorrect",
        "That function does not match the expected structure yet. Revisit the logic and try again.",
    )
