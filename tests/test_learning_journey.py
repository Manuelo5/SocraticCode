from pathlib import Path

from streamlit.testing.v1 import AppTest

import ai_tutor


APP_PATH = Path(__file__).parents[1] / "app.py"


def test_complete_scripted_learning_journey_and_restart(monkeypatch) -> None:
    monkeypatch.setenv("SOCRATICCODE_SCRIPTED_ONLY", "1")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key-not-a-real-credential")

    def unexpected_openai_client(**kwargs):
        raise AssertionError("Acceptance testing must not make live API requests.")

    monkeypatch.setattr(ai_tutor, "OpenAI", unexpected_openai_client)

    app = AppTest.from_file(str(APP_PATH)).run()
    progress = app.session_state["progress"]

    assert not app.exception
    assert app.title[0].value == "Exercise 1: Calculate an average"
    assert any("Scripted-only mode" in item.value for item in app.caption)
    assert next(item for item in app.button if item.key == "navigate_even").disabled
    assert next(item for item in app.button if item.key == "navigate_larger").disabled

    app.button(key="submit_average").click().run()
    assert not app.exception
    assert any(item.title == "Not correct yet" for item in app.warning)

    edited_draft = (
        "def calculate_average(numbers):\n"
        "    total = sum(numbers)\n"
        "    return total / 2\n"
    )
    app.text_area(key="code_average").set_value(edited_draft).run()
    for level in range(1, 5):
        app.button(key="hint_average").click().run()
        assert not app.exception
        assert app.text_area(key="code_average").value == edited_draft
        assert progress["hints_by_exercise"]["average"] == level
        assert any(
            item.title == f"Scripted fallback hint · level {level} of 4"
            for item in app.info
        )

    average_solution = (
        "def calculate_average(numbers):\n"
        "    return sum(numbers) / len(numbers)\n"
    )
    app.text_area(key="code_average").set_value(average_solution).run()
    app.button(key="submit_average").click().run()
    assert not app.exception
    assert "average" in progress["completed_exercises"]
    assert not next(item for item in app.button if item.key == "navigate_even").disabled

    app.button(key="navigate_even").click().run()
    assert app.title[0].value == "Exercise 2: Check whether a number is even"
    app.button(key="submit_even").click().run()
    assert any(item.title == "Not correct yet" for item in app.warning)
    app.button(key="hint_even").click().run()
    assert any(
        item.title == "Scripted fallback hint · level 1 of 4" for item in app.info
    )

    even_solution = (
        "def is_even(number):\n"
        "    return number % 2 == 0\n"
    )
    app.text_area(key="code_even").set_value(even_solution).run()
    app.button(key="submit_even").click().run()
    assert not app.exception
    assert "even" in progress["completed_exercises"]
    assert not next(item for item in app.button if item.key == "navigate_larger").disabled

    app.button(key="navigate_larger").click().run()
    assert app.title[0].value == "Solo Check: Return the larger number"
    assert not any(item.key == "hint_larger" for item in app.button)
    app.button(key="submit_larger").click().run()
    assert not app.exception
    assert progress["solo_check_passed"] is False
    assert any(item.title == "Not correct yet" for item in app.warning)

    solo_solution = (
        "def larger_of_two(first, second):\n"
        "    if first > second:\n"
        "        return first\n"
        "    return second\n"
    )
    app.text_area(key="code_larger").set_value(solo_solution).run()
    app.button(key="submit_larger").click().run()
    assert not app.exception
    assert progress["solo_check_passed"] is True
    assert app.title[0].value == "Your learning summary"
    metrics = {metric.label: metric.value for metric in app.metric}
    assert metrics["Exercises completed"] == "3"
    assert metrics["Hints requested"] == "5"
    assert metrics["Code submissions"] == "6"
    assert metrics["Solo Check"] == "Passed"

    app.button(key="restart_session").click().run()
    assert not app.exception
    assert app.title[0].value == "Exercise 1: Calculate an average"
    assert app.text_area(key="code_average").value == (
        "def calculate_average(numbers):\n"
        "    return sum(numbers) // len(numbers)\n"
    )
    assert "average" not in app.session_state["progress"]["completed_exercises"]
    assert any("0 of 3 exercises complete" in item.text for item in app.progress)
