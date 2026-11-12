README prose word count: approximately 560 words.

# SocraticCode — An AI Tutor That Teaches You to Think

SocraticCode is a local Streamlit prototype for helping beginner programmers reason through Python debugging tasks. It uses progressive scripted hints for two guided exercises, followed by a no-hint Solo Check. The tutor is deliberately not connected to an AI service in this phase.

## What works

- Three editable debugging tasks: calculate an average, check whether a number is even, and return the larger of two numbers.
- Four individually requested, progressively specific scripted hints for each guided task.
- Exercise 3 is an independent Solo Check with hints disabled. It unlocks only after the first two exercises are completed.
- Session progress tracks completed exercises, hints, submissions, and Solo Check outcome.
- Draft code is retained across Streamlit interactions and exercise navigation. The learner can restart the session.
- Submitted code is parsed and structurally compared with the reference function. It is never executed.
- A final summary reports session activity without presenting hint use as a learning score.

## Limitations and planned work

Structural AST comparison is not behavioral testing. It accepts only the expected function structure, so a logically correct alternative implementation may be marked incorrect. The validator does not run tests or untrusted code. Progress is kept in Streamlit session state and is not saved after the session ends.

OpenAI-powered contextual hints, API error handling, scripted fallback mode, and response-leakage safeguards are planned for Phase 3. Explain-back questions, adaptive hint fading, long-term analytics, and instructor features remain optional future work.

## Technology

- Python 3.11+
- Streamlit
- pytest
- Python's built-in `ast` module for non-executing structural checks

The OpenAI SDK remains listed in `requirements.txt` for the planned integration, but Phase 2 makes no API calls and requires no API key.

## Install and run

From the project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local address printed by Streamlit, usually `http://localhost:8501`.

## Run tests

Activate the virtual environment, then run:

```bash
python -m pytest -q
```

The tests cover exercise definitions, the hint ladder, structural validation and syntax errors, completion order, hint restrictions for the Solo Check, and submission/progress tracking.

Validation performed for Phase 2:

- `python -m pytest -q` — 13 tests passed.
- `mypy --ignore-missing-imports app.py exercises.py hint_controller.py evaluator.py progress_tracker.py` — no issues found.
- Python compilation check — passed.
- A headless Streamlit session started successfully; I checked the guided flow, sequential unlocking, disabled Solo Check hints, final summary, code draft retention, and session restart.

## Development record

- Phase 1: created the Streamlit app shell, dependency setup, README, and initial smoke test.
- Phase 2: added exercise definitions, scripted hints, safe AST comparison, session progress, sequential unlocking, the Solo Check, results summary, and focused unit tests. Validation results are listed above.
- Phase 3 is planned: integrate contextual OpenAI-generated hints with explicit error handling and safeguards.

The local project is under Git version control. The public repository's initial README commit is preserved in the integrated history. No code has been pushed to GitHub yet.

## AI assistance

AI coding assistance was used in the VS Code Copilot environment. Generated changes were checked against the requirements, exercised with pytest, and run in Streamlit. The code intentionally avoids executing learner submissions or calling a paid AI API in this phase.
