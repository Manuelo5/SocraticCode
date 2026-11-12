# Development record

## Phase 1 — Project setup

Created the local Streamlit app shell, dependency setup, environment example, README,
and initial app-title smoke test.

## Phase 2 — Core interactive prototype

Added three Python debugging exercises, the four-level scripted hint controller,
AST-based structural checking, exercise progression, session-only progress tracking,
the independent Solo Check, results summary, and focused unit tests.

## Phase 3 — AI tutor integration

Added an OpenAI Responses API adapter using a configurable model. Hints receive only
the exercise objective and description, current student code, level, and up to three
prior hints; the reference solution is excluded. AI calls occur only on an explicit
guided-exercise hint request, with a 20-second timeout, retries disabled, bounded
output tokens, and response storage disabled. Results are cached in session state.
Missing credentials, API errors, empty/oversized responses, and detected solution
leaks use labelled scripted hints. AI and scripted hints remain disabled for the
Solo Check.

The app reads `OPENAI_API_KEY` from the process environment, a local ignored `.env`
file loaded with python-dotenv, or Streamlit secrets. `OPENAI_MODEL` selects the
model; the default is `gpt-6-luna`.

Automated tests mock the OpenAI client; no live API call or paid model response is
claimed. Phase 3 validation: `python -m pytest -q` passed 29 tests, mypy reported
no issues in six application modules, and `compileall` completed successfully.
The headless Streamlit app loaded successfully through the local agent API, without
requesting a hint or making a live model call.

## Planned

Optional explain-back questions, adaptive hint fading, long-term performance
analytics, and instructor dashboards remain future work. The AST checker is
structural rather than behavioral; session progress is not persisted across sessions.
Prompt instructions and code checks cannot guarantee against every solution leak.

AI coding assistance was used through the VS Code Copilot environment. Suggestions
were reviewed against the requirements, tests, and local app startup.

Phase 3 changes are local and have not been pushed to GitHub. Push requires explicit
user approval.
