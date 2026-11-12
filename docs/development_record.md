# Development Record

## Phase 1 — Project setup

Created the local Streamlit application shell, dependency list, environment example,
README, and initial app-title smoke test.

## Phase 2 — Core interactive prototype

Added three Python debugging exercises, the four-level scripted hint controller,
AST-based structural checking, exercise progression, session-only progress tracking,
the independent Solo Check, and the final results summary. Added tests for exercise
content, hint progression, safe evaluation, unlocking, and Solo Check restrictions.

Validation performed on 11 November 2026:
- `python -m pytest -q`: 13 tests passed.
- `mypy --ignore-missing-imports app.py exercises.py hint_controller.py evaluator.py progress_tracker.py`:
  no issues found in five source files.
- `python -m compileall -q app.py exercises.py hint_controller.py evaluator.py progress_tracker.py tests`:
  completed successfully.
- A headless Streamlit run loaded successfully. The guided flow, exercise unlock
  order, Solo Check hint restriction, results summary, draft retention, and restart
  behavior were exercised through the local Streamlit agent API.

## Planned

- Phase 3: contextual AI-generated hints, API error handling, scripted fallback, and
  safeguards against overly revealing tutor responses.
- Later: optional explain-back prompts and adaptive assistance fading.

The local project is under Git version control. The public repository's initial
README commit is preserved in the integrated history. No code has been pushed to GitHub.
