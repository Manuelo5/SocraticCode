"""Streamlit interface for the SocraticCode interactive prototype."""

from __future__ import annotations

import os

import streamlit as st
from dotenv import load_dotenv
from streamlit.errors import StreamlitSecretNotFoundError

from ai_tutor import TutorHint, get_model_name
from evaluator import evaluate_submission
from exercises import EXERCISES, Exercise
from hint_controller import MAX_HINT_LEVEL, get_next_hint, request_next_hint
from progress_tracker import (
    can_access_exercise,
    create_progress,
    record_hint,
    record_submission,
    save_draft,
)


def get_app_title() -> str:
    return "SocraticCode — An AI Tutor That Teaches You to Think"


def _initialise_session() -> None:
    """Create learner state once; drafts live in progress outside widget state."""
    if "progress" not in st.session_state:
        st.session_state.progress = create_progress()
    st.session_state.setdefault("current_exercise", EXERCISES[0].id)
    st.session_state.setdefault("feedback", {})


def _save_code(exercise_id: str) -> None:
    """Keep drafts outside widget state so they survive hiding a text area."""
    progress = st.session_state.progress
    save_draft(progress, exercise_id, st.session_state[f"code_{exercise_id}"])
    st.session_state.feedback[exercise_id] = None


def _restart_session() -> None:
    """Clear app and widget state before the next run initializes fresh values."""
    for key in list(st.session_state):
        if not isinstance(key, str):
            continue
        if (
            key in {"progress", "current_exercise", "feedback"}
            or key.startswith("code_")
            or key.startswith("latest_hint_")
        ):
            del st.session_state[key]


def _select_exercise(exercise_id: str) -> None:
    st.session_state.current_exercise = exercise_id


def _show_sidebar() -> None:
    progress = st.session_state.progress
    with st.sidebar:
        st.header("Your progress")
        for index, exercise in enumerate(EXERCISES):
            complete = exercise.id in progress["completed_exercises"]
            accessible = can_access_exercise(index, progress)
            label = f"{'✓' if complete else f'{index + 1}.'} {exercise.title}"
            st.button(
                label,
                key=f"navigate_{exercise.id}",
                on_click=_select_exercise,
                args=(exercise.id,),
                disabled=not accessible,
                width="stretch",
            )

        st.progress(
            len(progress["completed_exercises"]) / len(EXERCISES),
            text=f"{len(progress['completed_exercises'])} of {len(EXERCISES)} exercises complete",
        )
        st.divider()
        st.caption("Guided hints: AI when configured; scripted fallback if unavailable.")
        st.button(
            "Restart learning session",
            key="restart_session",
            on_click=_restart_session,
            width="stretch",
        )


def _show_hint(exercise: Exercise) -> None:
    progress = st.session_state.progress
    used = progress["hints_by_exercise"][exercise.id]
    next_hint = get_next_hint(exercise, used)
    if next_hint is None:
        st.info("You have used all four hints for this exercise. Try applying what you have learned.")
        return

    level, _ = next_hint
    cached = progress["hint_cache"][exercise.id].get(level)
    if cached is None:
        code = st.session_state[f"code_{exercise.id}"]
        save_draft(progress, exercise.id, code)
        previous_hints = [
            item["text"] for item in progress["hint_history"][exercise.id]
        ]
        with st.spinner("Preparing your next hint..."):
            hint = request_next_hint(
                exercise,
                code,
                used,
                previous_hints,
                api_key=_get_api_key(),
                model=get_model_name(),
            )
        if hint is None:
            return
        cached = {
            "level": hint.level,
            "text": hint.text,
            "source": hint.source,
            "error": hint.error,
        }
        progress["hint_cache"][exercise.id][level] = cached
    else:
        hint = TutorHint(
            level=cached["level"],
            text=cached["text"],
            source=cached["source"],
            error=cached["error"],
        )

    if not record_hint(progress, exercise):
        return
    st.session_state.feedback[exercise.id] = None
    progress["hint_history"][exercise.id].append(cached)


def _get_api_key() -> str | None:
    """Read credentials from the environment or Streamlit secrets, never log them."""
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if api_key:
        return api_key
    try:
        api_key = str(st.secrets["OPENAI_API_KEY"]).strip()
    except (KeyError, StreamlitSecretNotFoundError):
        return None
    return api_key or None


def _show_results() -> None:
    progress = st.session_state.progress
    st.title("Your learning summary")
    st.write(
        "This summary describes this session only. One Solo Check is not evidence "
        "of long-term learning improvement."
    )
    first, second = st.columns(2)
    first.metric("Exercises completed", len(progress["completed_exercises"]))
    second.metric("Hints requested", sum(progress["hints_by_exercise"].values()))
    third, fourth = st.columns(2)
    third.metric(
        "Code submissions",
        sum(progress["submissions_by_exercise"].values()),
    )
    fourth.metric(
        "Solo Check",
        "Passed" if progress["solo_check_passed"] else "Not passed",
    )
    st.success("You completed all three exercises. Well done!")
    st.info(
        "The hint count is a usage measure, not a learning score. The Solo Check "
        "captures performance on one independent task only."
    )


def _show_exercise(exercise: Exercise) -> None:
    progress = st.session_state.progress
    st.title(exercise.title)
    if exercise.is_solo_check:
        st.warning(
            "Solo Check — independent challenge. AI hints, scripted hints, and AI chat are disabled.",
            icon=":material/lock:",
        )
    else:
        st.caption(
            "Progressive guidance: AI-generated when configured; scripted hints are used as fallback."
        )
        st.caption(
            "When AI is configured, requesting a hint sends this exercise's current code to OpenAI."
        )

    st.write(exercise.description)
    with st.container(border=True):
        st.subheader("Expected behaviour")
        st.write(exercise.expected_behaviour)

    code_key = f"code_{exercise.id}"
    if code_key not in st.session_state:
        st.session_state[code_key] = progress["drafts"][exercise.id]
    st.text_area(
        "Your Python code",
        key=code_key,
        height=240,
        help="Edit the function, then submit it for structural checking.",
        disabled=exercise.id in progress["completed_exercises"],
        on_change=_save_code,
        args=(exercise.id,),
    )

    result = st.session_state.feedback.get(exercise.id)
    if result:
        if result.status == "syntax_error":
            st.error(f"Syntax error: {result.message}", title="Check your Python syntax")
        elif result.status == "correct":
            st.success(result.message, title="Correct")
        else:
            st.warning(result.message, title="Not correct yet")

    if exercise.id in progress["completed_exercises"]:
        st.success("This exercise is complete. You can move on or review it.")

    button_col, hint_col = st.columns([1, 1], vertical_alignment="bottom")
    with button_col:
        if st.button(
            "Check my code",
            type="primary",
            key=f"submit_{exercise.id}",
            disabled=exercise.id in progress["completed_exercises"],
        ):
            code = st.session_state[f"code_{exercise.id}"]
            save_draft(progress, exercise.id, code)
            submission = evaluate_submission(exercise, code)
            record_submission(progress, exercise, submission.status == "correct")
            st.session_state.feedback[exercise.id] = submission
            st.rerun()

    with hint_col:
        if not exercise.is_solo_check:
            used = progress["hints_by_exercise"][exercise.id]
            if st.button(
                f"Request hint ({used}/{MAX_HINT_LEVEL})",
                key=f"hint_{exercise.id}",
                disabled=used >= MAX_HINT_LEVEL or exercise.id in progress["completed_exercises"],
            ):
                _show_hint(exercise)

    if not exercise.is_solo_check:
        for item in progress["hint_history"][exercise.id]:
            if item["source"] == "ai":
                title = f"AI-generated hint · level {item['level']} of {MAX_HINT_LEVEL}"
            else:
                title = f"Scripted fallback hint · level {item['level']} of {MAX_HINT_LEVEL}"
            with st.container(border=True):
                st.info(item["text"], title=title)
                if item["error"]:
                    st.caption(item["error"])
        st.caption(
            "AI safeguards reduce solution leakage but cannot guarantee that every generated response is safe."
        )

    if exercise.is_solo_check:
        st.caption(
            f"Solo Check submissions: {progress['submissions_by_exercise'][exercise.id]}"
        )

    with st.expander("How code is checked"):
        st.write(
            "The app parses your code and compares the target function's syntax tree "
            "with the reference structure. It never runs submitted code. This is not "
            "unit-test execution: another logically correct implementation may not "
            "match the expected structure and may be marked incorrect."
        )


def main() -> None:
    load_dotenv()
    st.set_page_config(
        page_title="SocraticCode",
        page_icon=":material/school:",
        layout="wide",
    )
    _initialise_session()
    _show_sidebar()

    progress = st.session_state.progress
    if len(progress["completed_exercises"]) == len(EXERCISES):
        _show_results()
        return

    exercise_id = st.session_state.current_exercise
    exercise = next(item for item in EXERCISES if item.id == exercise_id)
    if not can_access_exercise(EXERCISES.index(exercise), progress):
        exercise = EXERCISES[0]
        st.session_state.current_exercise = exercise.id
    _show_exercise(exercise)


if __name__ == "__main__":
    main()
