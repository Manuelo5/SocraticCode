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
claimed. Phase 3 validation: `python -m pytest -q` passed 32 tests, mypy reported
no issues in six application modules, and `compileall` completed successfully.

## Phase 3 final verification

The installed OpenAI Python SDK was version 3.49.0; the installed Responses API
signature was inspected, and the request uses the supported `client.responses.create`
pattern. Official OpenAI documentation lists `gpt-6-luna` as supporting the Responses
API. No valid API key was configured, so model availability for this account and
live hint quality were not verified and no billable request was made. A local `.env`
was created from `.env.example` with its placeholder only.

Offline UI tests verified that missing credentials show a labelled scripted fallback
without crashing and retain code/progress. Solo Check UI tests verified that hint
controls are absent, incorrect and correct submissions receive feedback, and the
completion outcome is recorded. The mocked AI tests do not establish live response
quality.

Verification caught and fixed a setup edge case: `.env` was created from the example
with its placeholder, and the app now treats `your_api_key_here` as missing so it
cannot send the placeholder to OpenAI. The updated regression test confirms the
placeholder path uses the scripted fallback without constructing an API client.

## Planned

Optional explain-back questions, adaptive hint fading, long-term performance
analytics, and instructor dashboards remain future work. The AST checker is
structural rather than behavioral; session progress is not persisted across sessions.
Prompt instructions and code checks cannot guarantee against every solution leak.

AI coding assistance was used through the VS Code Copilot environment. Suggestions
were reviewed against the requirements, tests, and local app startup.

## Phase 4 — Acceptance and evaluation preparation

The request was to verify the complete interactive journey without making any live
OpenAI calls or claiming participant findings. Inspection identified three clarity
improvements: the hint mode was described generically, the sidebar did not explain
why the Solo Check was locked, and the code-editor help did not explicitly state
that submitted code is not executed. The interface now identifies the active hint
mode, explains the unlock order, and states the evaluator's no-execution boundary.

Added `SOCRATICCODE_SCRIPTED_ONLY=1` as an offline safeguard. It bypasses both
environment and Streamlit credentials without changing saved keys, making manual
acceptance and screenshot capture safe even when a key is configured. The UI
explicitly labels this mode.

Added a Streamlit `AppTest` journey that starts in scripted-only mode and exercises
the app from Exercise 1 through restart. It submitted incorrect and corrected
answers, requested all four hints one at a time, checked that edits survive hint
requests, unlocked Exercise 2 and the Solo Check, confirmed no Solo Check hint
control, checked the dashboard totals (3 completed exercises, 5 hints, 6
submissions, Solo Check passed), and verified restart resets the draft and
completion state. The API client was guarded so a live request would fail the
test. The acceptance test passed; the complete suite passed 33 tests. Mypy
reported no issues in the six application modules, and `compileall` completed
successfully. No participant sessions, live AI responses, or learning outcomes
were tested or claimed.

Added `docs/usability-evaluation.md` with a three-participant plan, consent/privacy
checklist, tasks, observation and post-task questions, and a blank results template.
Added `docs/storyboards.md` with three reproducible scripted-mode screenshot
scenarios. README and this record now distinguish implemented, simulated,
unverified, and unevaluated components. These documents are evaluation materials;
they do not report fabricated observations.

The Phase 3 commits `128fd3a` and `2a51f8f` are included in the synchronized
`origin/main` history. Phase 4 changes are local until explicitly reviewed and
pushed; no push is authorized by this work.
