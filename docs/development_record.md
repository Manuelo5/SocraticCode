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

## Final refinement — bounded AST validation

The user reported a real issue from manual testing: the Solo Check solution with
an explicit `else` branch was rejected even though it returns the larger input.
The reported session completed all three exercises, requested four scripted hints,
made 13 submissions, and passed the Solo Check. Those are user-reported manual
results, not results from an additional participant study.

The cause was exact whole-function AST equality against a single reference
implementation. The submitted `if` statement had an `else` block in its AST,
while the reference placed the fallback `return` after the `if`; the two forms
behave equivalently, but their ASTs differ.

Replaced exact-reference matching with exercise-specific, bounded AST recognizers.
They parse the submission and inspect only whitelisted syntax; no submitted code
is imported, evaluated, or executed. The documented supported patterns are:

- **Average:** direct sum divided by list length, or the same operations assigned
  to simple local variables before the return. The known floor-division version
  is classified as incorrect. Other expressions outside the recognized form are
  unsupported rather than being asserted incorrect.
- **Even check:** a direct modulo-by-two expression compared with an integer
  constant. The checker accepts comparisons whose results distinguish remainder
  zero from remainder one, including reversed operands, and boolean negation of
  the modulo expression. A recognizable predicate that does not distinguish
  those two remainders is classified as incorrect.
- **Solo Check:** a two-way `if` with either an explicit `else` or a following
  fallback return, an inline conditional, or a call to built-in `max` with both
  inputs. Conditional branches must return one of the inputs, and the checker
  checks the branch logic for either ordering and a tie using its own static
  comparison handling; it never runs the student's function.

Syntax errors retain distinct line-aware feedback. Recognizable incorrect logic
gets a review-your-logic message; valid structures outside these patterns get an
unsupported-structure message and are not described as incorrect. The UI's
“How code is checked” expander documents the supported pattern families and
limitations without exposing a complete reference function.

Regression tests cover all reference solutions, average aliases, modulo-based
equivalents, the explicit-`else` Solo Check solution, an inline conditional,
`max`, a smaller-number implementation, incorrect logic, syntax errors, an
unsupported-but-valid expression, and a source snippet that would create a file
if it were executed. Existing AppTests continue to cover progression and the
absence of Solo Check hints. The full suite passed **42 tests**; mypy reported no
issues in the six application modules, and `compileall` completed successfully.

This refinement is intended to improve feedback quality and learner trust: a
valid but unrecognized structure is no longer labelled incorrect, and syntax or
logic feedback gives a clearer next step. It supports error recovery without
claiming that the evaluator proves semantic equivalence for all Python programs.
A correct solution outside the whitelist can still be marked unsupported.
