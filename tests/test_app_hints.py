from pathlib import Path

from streamlit.testing.v1 import AppTest

import hint_controller
import ai_tutor
from ai_tutor import TutorHint


APP_PATH = Path(__file__).parents[1] / "app.py"


def test_hint_click_preserves_edited_code_and_displays_generated_hint(
    monkeypatch,
) -> None:
    calls = []

    def fake_generate(*args, **kwargs) -> TutorHint:
        calls.append((args, kwargs))
        return TutorHint(1, "Consider what kind of division keeps a fraction.", "ai")

    monkeypatch.setattr(hint_controller, "generate_ai_hint", fake_generate)

    app = AppTest.from_file(str(APP_PATH)).run()
    draft = "def calculate_average(numbers):\n    total = sum(numbers)\n    return total / len(numbers)\n"
    app.text_area(key="code_average").set_value(draft).run()
    app.button(key="hint_average").click().run()
    app.run()

    assert not app.exception
    assert app.text_area(key="code_average").value == draft
    assert any("AI-generated hint" in item.title for item in app.info)
    assert len(calls) == 1
    assert app.session_state["progress"]["hints_by_exercise"]["average"] == 1


def test_solo_check_ui_has_no_hint_button(monkeypatch) -> None:
    def unexpected_generate(*args, **kwargs) -> TutorHint:
        raise AssertionError("The Solo Check must never request AI hints.")

    monkeypatch.setattr(hint_controller, "generate_ai_hint", unexpected_generate)

    app = AppTest.from_file(str(APP_PATH)).run()
    progress = app.session_state["progress"]
    progress["completed_exercises"] = ["average", "even"]
    app.session_state["current_exercise"] = "larger"
    app.run()

    assert not app.exception
    assert any("AI hints, scripted hints" in item.value for item in app.warning)
    assert not any(button.key == "hint_larger" for button in app.button)


def test_missing_key_uses_scripted_fallback_in_app(
    monkeypatch,
) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    def unexpected_client(**kwargs):
        raise AssertionError("The .env example placeholder must not call OpenAI.")

    monkeypatch.setattr(ai_tutor, "OpenAI", unexpected_client)
    app = AppTest.from_file(str(APP_PATH)).run()

    app.button(key="hint_average").click().run()

    assert not app.exception
    assert app.session_state["progress"]["hints_by_exercise"]["average"] == 1
    assert any("Scripted fallback hint" in item.title for item in app.info)
    assert any("No API key is configured" in item.value for item in app.caption)


def test_solo_check_submission_records_incorrect_and_success_outcomes(
    monkeypatch,
) -> None:
    def unexpected_generate(*args, **kwargs) -> TutorHint:
        raise AssertionError("The Solo Check must never call the AI tutor.")

    monkeypatch.setattr(hint_controller, "generate_ai_hint", unexpected_generate)
    app = AppTest.from_file(str(APP_PATH)).run()
    progress = app.session_state["progress"]
    progress["completed_exercises"] = ["average", "even"]
    app.session_state["current_exercise"] = "larger"
    app.run()

    assert not any(button.key == "hint_larger" for button in app.button)
    app.button(key="submit_larger").click().run()
    assert not app.exception
    assert progress["solo_check_passed"] is False
    assert progress["submissions_by_exercise"]["larger"] == 1
    assert any("Not correct yet" in item.title for item in app.warning)

    solution = (
        "def larger_of_two(first, second):\n"
        "    if first > second:\n"
        "        return first\n"
        "    return second\n"
    )
    app.text_area(key="code_larger").set_value(solution).run()
    app.button(key="submit_larger").click().run()

    assert not app.exception
    assert progress["solo_check_passed"] is True
    assert progress["submissions_by_exercise"]["larger"] == 2
    assert any(metric.label == "Solo Check" and metric.value == "Passed" for metric in app.metric)
