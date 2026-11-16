"""Safe, deterministic checking of supported solution patterns without execution."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Literal

from exercises import Exercise

EvaluationStatus = Literal["correct", "incorrect", "syntax_error", "unsupported"]
ExpressionSignature = tuple[object, ...]


@dataclass(frozen=True)
class EvaluationResult:
    status: EvaluationStatus
    message: str


def _target_function(source: str, function_name: str) -> ast.FunctionDef | None:
    """Parse a function-only submission and find its synchronous target function."""
    tree = ast.parse(source)
    if len(tree.body) != 1 or not isinstance(tree.body[0], ast.FunctionDef):
        return None
    function = tree.body[0]
    return function if function.name == function_name else None


def evaluate_submission(exercise: Exercise, source: str) -> EvaluationResult:
    """Check a bounded set of AST patterns. Submitted code is never executed."""
    try:
        submitted = _target_function(source, exercise.function_name)
    except SyntaxError as exc:
        line = f" on line {exc.lineno}" if exc.lineno is not None else ""
        return EvaluationResult(
            "syntax_error",
            f"Python syntax error{line}. Fix it and try again.",
        )
    try:
        reference = _target_function(
            exercise.reference_solution, exercise.function_name
        )
    except SyntaxError as exc:
        raise ValueError(
            f"Exercise {exercise.id!r} has an invalid reference solution."
        ) from exc

    if reference is None:
        raise ValueError(f"Exercise {exercise.id!r} has an invalid reference function.")
    if submitted is None or not _has_supported_signature(submitted, reference):
        return _unsupported_result()

    if exercise.id == "average":
        result = _check_average(submitted)
    elif exercise.id == "even":
        result = _check_even(submitted)
    elif exercise.id == "larger":
        result = _check_larger(submitted)
    else:
        raise ValueError(f"No AST validation patterns are defined for {exercise.id!r}.")

    if result is None:
        return _unsupported_result()
    if not result:
        return EvaluationResult(
            "incorrect",
            "This recognizable logic does not meet the expected behavior yet. "
            "Review your calculation or condition and try again.",
        )
    return EvaluationResult(
        "correct",
        "Your logic matches a supported solution pattern. You can move on to the next exercise.",
    )


def _unsupported_result() -> EvaluationResult:
    return EvaluationResult(
        "unsupported",
        "This code uses a structure the checker cannot verify safely. "
        "Try one of the supported patterns described below. Your code was not run.",
    )


def _has_supported_signature(
    submitted: ast.FunctionDef, reference: ast.FunctionDef
) -> bool:
    return (
        not submitted.decorator_list
        and submitted.returns is None
        and submitted.type_comment is None
        and ast.dump(submitted.args, include_attributes=False)
        == ast.dump(reference.args, include_attributes=False)
    )


def _check_average(function: ast.FunctionDef) -> bool | None:
    """Accept sum(numbers) / len(numbers), including simple local aliases."""
    if not function.body or not isinstance(function.body[-1], ast.Return):
        return None
    aliases: dict[str, ExpressionSignature] = {}
    argument_names = {argument.arg for argument in function.args.args}
    for statement in function.body[:-1]:
        if (
            not isinstance(statement, ast.Assign)
            or len(statement.targets) != 1
            or not isinstance(statement.targets[0], ast.Name)
            or statement.targets[0].id in argument_names | {"sum", "len"}
            or statement.targets[0].id in aliases
        ):
            return None
        signature = _average_expression(statement.value, aliases)
        if signature is None:
            return None
        aliases[statement.targets[0].id] = signature

    returned = function.body[-1]
    if returned.value is None:
        return None
    signature = _average_expression(returned.value, aliases)
    if signature is None:
        return None
    numerator = ("call", "sum", ("name", "numbers"))
    denominator = ("call", "len", ("name", "numbers"))
    if signature == ("divide", numerator, denominator):
        return True
    if signature == ("floor_divide", numerator, denominator):
        return False
    return None


def _average_expression(
    expression: ast.expr, aliases: dict[str, ExpressionSignature]
) -> ExpressionSignature | None:
    if isinstance(expression, ast.Name):
        return aliases.get(expression.id, ("name", expression.id))
    if isinstance(expression, ast.Constant) and type(expression.value) in (int, float):
        return ("constant", type(expression.value).__name__, expression.value)
    if isinstance(expression, ast.Call):
        if (
            not isinstance(expression.func, ast.Name)
            or expression.func.id not in {"sum", "len"}
            or len(expression.args) != 1
            or expression.keywords
        ):
            return None
        argument = _average_expression(expression.args[0], aliases)
        return ("call", expression.func.id, argument) if argument is not None else None
    if isinstance(expression, ast.BinOp):
        operator_name = _arithmetic_operator_name(expression.op)
        left = _average_expression(expression.left, aliases)
        right = _average_expression(expression.right, aliases)
        if operator_name is None or left is None or right is None:
            return None
        return (operator_name, left, right)
    return None


def _arithmetic_operator_name(operator: ast.operator) -> str | None:
    operators: tuple[tuple[type[ast.operator], str], ...] = (
        (ast.Add, "add"),
        (ast.Sub, "subtract"),
        (ast.Mult, "multiply"),
        (ast.Div, "divide"),
        (ast.FloorDiv, "floor_divide"),
        (ast.Mod, "modulo"),
    )
    return next(
        (name for operator_type, name in operators if isinstance(operator, operator_type)),
        None,
    )


def _check_even(function: ast.FunctionDef) -> bool | None:
    """Recognize equivalent tests for the two possible remainders modulo two."""
    if len(function.body) != 1 or not isinstance(function.body[0], ast.Return):
        return None
    expression = function.body[0].value
    if expression is None:
        return None
    if isinstance(expression, ast.UnaryOp) and isinstance(expression.op, ast.Not):
        return _is_remainder_modulo_two(expression.operand)
    if _is_remainder_modulo_two(expression):
        return False
    if not isinstance(expression, ast.Compare) or len(expression.ops) != 1:
        return None

    left_is_remainder = _is_remainder_modulo_two(expression.left)
    right_is_remainder = _is_remainder_modulo_two(expression.comparators[0])
    if left_is_remainder == right_is_remainder:
        return None
    constant_node = (
        expression.comparators[0] if left_is_remainder else expression.left
    )
    if not isinstance(constant_node, ast.Constant) or type(constant_node.value) is not int:
        return None

    result_for_even = _compare_integers(
        0 if left_is_remainder else constant_node.value,
        expression.ops[0],
        constant_node.value if left_is_remainder else 0,
    )
    result_for_odd = _compare_integers(
        1 if left_is_remainder else constant_node.value,
        expression.ops[0],
        constant_node.value if left_is_remainder else 1,
    )
    if result_for_even is None or result_for_odd is None:
        return None
    return result_for_even and not result_for_odd


def _is_remainder_modulo_two(expression: ast.expr) -> bool:
    return (
        isinstance(expression, ast.BinOp)
        and isinstance(expression.op, ast.Mod)
        and isinstance(expression.left, ast.Name)
        and expression.left.id == "number"
        and isinstance(expression.right, ast.Constant)
        and type(expression.right.value) is int
        and expression.right.value == 2
    )


def _compare_integers(
    left: int, operator: ast.cmpop, right: int
) -> bool | None:
    if isinstance(operator, ast.Eq):
        return left == right
    if isinstance(operator, ast.NotEq):
        return left != right
    if isinstance(operator, ast.Lt):
        return left < right
    if isinstance(operator, ast.LtE):
        return left <= right
    if isinstance(operator, ast.Gt):
        return left > right
    if isinstance(operator, ast.GtE):
        return left >= right
    return None


def _check_larger(function: ast.FunctionDef) -> bool | None:
    """Validate two-way conditional returns against representative orderings."""
    if (
        len(function.body) == 1
        and isinstance(function.body[0], ast.Return)
        and _is_max_call(function.body[0].value)
    ):
        return True

    branches = _larger_branches(function)
    if branches is None:
        return None
    condition, when_true, when_false = branches
    comparison = _larger_comparison(condition)
    true_name = _returned_input(when_true)
    false_name = _returned_input(when_false)
    if comparison is None or true_name is None or false_name is None:
        return None

    for first, second in ((2, 1), (1, 2), (1, 1)):
        left = first if comparison[0] == "first" else second
        right = first if comparison[1] == "first" else second
        predicate = _compare_integers(left, comparison[2], right)
        if predicate is None:
            return None
        result_name = true_name if predicate else false_name
        result_value = first if result_name == "first" else second
        if result_value != max(first, second):
            return False
    return True


def _is_max_call(expression: ast.expr | None) -> bool:
    return (
        isinstance(expression, ast.Call)
        and isinstance(expression.func, ast.Name)
        and expression.func.id == "max"
        and len(expression.args) == 2
        and not expression.keywords
        and {argument.id for argument in expression.args if isinstance(argument, ast.Name)}
        == {"first", "second"}
        and all(isinstance(argument, ast.Name) for argument in expression.args)
    )


def _larger_branches(
    function: ast.FunctionDef,
) -> tuple[ast.expr, ast.expr, ast.expr] | None:
    if len(function.body) == 1 and isinstance(function.body[0], ast.Return):
        expression = function.body[0].value
        if isinstance(expression, ast.IfExp):
            return expression.test, expression.body, expression.orelse
        return None
    if not function.body or not isinstance(function.body[0], ast.If):
        return None
    conditional = function.body[0]
    if len(conditional.body) != 1 or not isinstance(conditional.body[0], ast.Return):
        return None
    if conditional.orelse:
        if len(function.body) != 1 or len(conditional.orelse) != 1:
            return None
        if not isinstance(conditional.orelse[0], ast.Return):
            return None
        fallback = conditional.orelse[0]
    else:
        if len(function.body) != 2 or not isinstance(function.body[1], ast.Return):
            return None
        fallback = function.body[1]
    if conditional.body[0].value is None or fallback.value is None:
        return None
    return conditional.test, conditional.body[0].value, fallback.value


def _larger_comparison(
    expression: ast.expr,
) -> tuple[str, str, ast.cmpop] | None:
    if not isinstance(expression, ast.Compare) or len(expression.ops) != 1:
        return None
    left, right = expression.left, expression.comparators[0]
    if not isinstance(left, ast.Name) or left.id not in {"first", "second"}:
        return None
    if not isinstance(right, ast.Name) or right.id not in {"first", "second"}:
        return None
    return left.id, right.id, expression.ops[0]


def _returned_input(expression: ast.expr) -> str | None:
    if isinstance(expression, ast.Name) and expression.id in {"first", "second"}:
        return expression.id
    return None
