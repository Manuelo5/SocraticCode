import json
from types import SimpleNamespace

import openai
import pytest

import ai_tutor
from exercises import EXERCISES


class FakeResponses:
    def __init__(self, response_text: str = "Think about what the remainder tells you."):
        self.response_text = response_text
        self.calls: list[dict[str, object]] = []
        self.error: Exception | None = None

    def create(self, **kwargs: object) -> SimpleNamespace:
        self.calls.append(kwargs)
        if self.error:
            raise self.error
        return SimpleNamespace(output_text=self.response_text)


class FakeClient:
    def __init__(self, responses: FakeResponses):
        self.responses = responses

    def __enter__(self) -> "FakeClient":
        return self

    def __exit__(self, *args: object) -> None:
        return None


def test_hint_request_contains_context_and_excludes_reference_solution() -> None:
    exercise = EXERCISES[1]
    request = json.loads(
        ai_tutor.build_hint_input(
            exercise,
            exercise.starter_code,
            2,
            ["A previous hint from this exercise."],
        )
    )

    assert request["exercise_title"] == exercise.title
    assert request["exercise_description"] == exercise.description
    assert request["learning_objective"] == exercise.learning_objective
    assert request["student_code"] == exercise.starter_code
    assert request["hint_level"] == 2
    assert request["previous_hints"] == ["A previous hint from this exercise."]
    assert exercise.reference_solution not in json.dumps(request)


@pytest.mark.parametrize(
    ("level", "expected_phrase"),
    [
        (1, "Conceptual hint"),
        (2, "Diagnostic hint"),
        (3, "Logical hint"),
        (4, "Partial implementation hint"),
    ],
)
def test_each_hint_level_has_its_own_assistance_limit(
    level: int, expected_phrase: str
) -> None:
    assert expected_phrase in ai_tutor.LEVEL_GUIDANCE[level]


def test_ai_request_uses_configured_model_timeout_limits_and_context(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    responses = FakeResponses()
    constructor_args: dict[str, object] = {}

    def fake_openai(**kwargs: object) -> FakeClient:
        constructor_args.update(kwargs)
        return FakeClient(responses)

    monkeypatch.setattr(ai_tutor, "OpenAI", fake_openai)
    result = ai_tutor.generate_hint(
        EXERCISES[0],
        "def calculate_average(numbers):\n    return 3\n",
        1,
        api_key="test-key",
        model="test-model",
    )

    assert result.source == "ai"
    assert result.text == "Think about what the remainder tells you."
    assert constructor_args == {
        "api_key": "test-key",
        "timeout": ai_tutor.REQUEST_TIMEOUT_SECONDS,
        "max_retries": 0,
    }
    call = responses.calls[0]
    assert call["model"] == "test-model"
    assert call["max_output_tokens"] == ai_tutor.MAX_OUTPUT_TOKENS
    assert call["reasoning"] == {"effort": "none"}
    assert call["store"] is False
    assert "student_code" in str(call["input"])
    assert "reference_solution" not in str(call["input"])


def test_missing_api_key_uses_scripted_fallback_without_creating_client(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def unexpected_client(**kwargs: object) -> FakeClient:
        raise AssertionError("OpenAI client must not be constructed without an API key.")

    monkeypatch.setattr(ai_tutor, "OpenAI", unexpected_client)
    exercise = EXERCISES[0]
    result = ai_tutor.generate_hint(
        exercise, exercise.starter_code, 1, api_key=None
    )

    assert result.source == "scripted"
    assert result.text == exercise.hints[0]
    assert "No API key" in (result.error or "")


def test_timeout_uses_scripted_fallback_without_retrying(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    responses = FakeResponses()
    responses.error = TimeoutError("private timeout details")
    client_creations = 0

    def fake_openai(**kwargs: object) -> FakeClient:
        nonlocal client_creations
        client_creations += 1
        return FakeClient(responses)

    monkeypatch.setattr(ai_tutor, "OpenAI", fake_openai)
    exercise = EXERCISES[0]
    result = ai_tutor.generate_hint(
        exercise, exercise.starter_code, 1, api_key="test-key"
    )

    assert result.source == "scripted"
    assert result.text == exercise.hints[0]
    assert client_creations == 1
    assert "private timeout details" not in (result.error or "")


def test_openai_error_uses_scripted_fallback_without_exposing_exception(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    responses = FakeResponses()
    responses.error = openai.OpenAIError("private diagnostic detail")
    monkeypatch.setattr(ai_tutor, "OpenAI", lambda **kwargs: FakeClient(responses))

    exercise = EXERCISES[0]
    result = ai_tutor.generate_hint(
        exercise, exercise.starter_code, 2, api_key="test-key"
    )

    assert result.source == "scripted"
    assert result.text == exercise.hints[1]
    assert "private diagnostic detail" not in (result.error or "")


def test_solution_leak_is_withheld_and_replaced_with_scripted_hint(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    exercise = EXERCISES[0]
    leaked = f"Here is the answer:\n```python\n{exercise.reference_solution}```"
    responses = FakeResponses(leaked)
    monkeypatch.setattr(ai_tutor, "OpenAI", lambda **kwargs: FakeClient(responses))

    result = ai_tutor.generate_hint(
        exercise, exercise.starter_code, 4, api_key="test-key"
    )

    assert result.source == "scripted"
    assert result.text == exercise.hints[3]
    assert "withheld" in (result.error or "")


def test_syntax_equivalent_solution_with_comments_is_withheld() -> None:
    exercise = EXERCISES[0]
    formatted_solution = (
        "```python\n"
        "# Here is the full answer\n"
        "def calculate_average(numbers):\n"
        "    return sum(numbers) / len(numbers)\n"
        "```"
    )
    assert ai_tutor.reveals_reference_solution(
        formatted_solution, exercise.reference_solution
    )


def test_hint_input_rejects_excessively_long_student_code() -> None:
    with pytest.raises(ValueError, match="input limit"):
        ai_tutor.build_hint_input(EXERCISES[0], "x" * (ai_tutor.MAX_STUDENT_CODE_CHARS + 1), 1)
