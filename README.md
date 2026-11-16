README prose word count: approximately 600 words.

# SocraticCode — An AI Tutor That Teaches You to Think

SocraticCode is a functional interactive tutoring prototype for beginner Python debugging. Its two guided exercises use a four-level scripted hint ladder by default, with an OpenAI integration available when credentials are configured. Live AI behavior has not been verified. Exercise 3 is an independent Solo Check with all hint controls disabled.

## Project scope

- **Implemented:** Streamlit exercise flow, scripted hints and fallback, AST-based structural checking, progression, session dashboard, restart, and mocked OpenAI integration.
- **Simulated for testing:** AI responses are mocked in automated tests; acceptance and storyboard runs can force scripted-only mode.
- **Unverified:** Live OpenAI account/model access and genuine AI hint quality. Do not treat the prototype as a verified live AI tutor.
- **Not evaluated yet:** Usability with participants or learning outcomes. See the [usability evaluation plan](docs/usability-evaluation.md) and [storyboards](docs/storyboards.md).

## What works

- Three editable debugging tasks: calculate an average, check whether a number is even, and return the larger of two numbers.
- Students request one hint at a time. The tutor sees the current exercise, learning objective, current code, requested level and earlier hints.
- AI output is labelled AI-generated. Missing credentials, API failures, empty responses, oversized responses and detected full-solution leaks use a clearly labelled scripted fallback.
- One hint result is cached per exercise and level in the current Streamlit session. Ordinary reruns do not make model requests.
- Only an explicit guided-hint request sends the current exercise code and minimal exercise context to OpenAI; no personal information is added.
- The first two exercises must be completed before the Solo Check unlocks. The Solo Check has no AI hints, scripted hints or chat.
- Progress, code drafts, hint history, submissions and Solo Check outcome are stored in session state.
- The evaluator uses bounded, exercise-specific AST patterns. It never executes student code and reports unrecognized structures as unsupported rather than incorrect.

## Limitations

Prompt instructions and output checks reduce the chance of a complete solution leak but cannot guarantee the model will never reveal one. The local safeguard detects verbatim solution text and syntax-equivalent functions in code blocks; it cannot detect every semantically equivalent answer. The code evaluator recognizes only documented patterns and is not behavioral testing; a correct solution outside those patterns may be marked unsupported. Progress is session-only. Live AI behavior was not tested during development; automated API tests use mocks.

## Phase 3 verification status

The installed OpenAI Python SDK is version 3.49.0, and the Responses API call shape was checked against the installed SDK. OpenAI's current [GPT-6 Luna model documentation](https://developers.openai.com/api/docs/models/gpt-6-luna) lists the Responses endpoint as supported. This does not confirm that the model is enabled for your API account. No valid key was configured during verification, so account access and live AI hints could not be tested. The local `.env` was created from `.env.example` and still contains only its placeholder.

The complete mocked/offline test suite passed **33 tests**. It covers AI request parameters, fallback behavior, hint caching and code preservation, and Solo Check restrictions. No live or billable API calls were made. Verification also caught and fixed a configuration edge case: the example `your_api_key_here` value is now treated as missing, so it cannot trigger an API request.

## Technology

- Python 3.11+
- Streamlit
- OpenAI Python SDK and the Responses API
- pytest and Python's built-in `ast` module

## Install and run

From the project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp -n .env.example .env
```

Get an API key from the [OpenAI API keys page](https://platform.openai.com/api-keys). In VS Code, open the project folder, select `.env` in Explorer (use **File → Open File** if hidden files are not visible), and replace only `your_api_key_here` with your key. Do not paste the key into chat or commit `.env`. The `-n` option leaves an existing `.env` unchanged; edit that file if you already have one. API usage can incur charges. `OPENAI_MODEL` defaults to `gpt-6-luna`, as listed in current official model documentation, but must be available to your API account. Alternatively, configure `OPENAI_API_KEY` in `.streamlit/secrets.toml` as `OPENAI_API_KEY = "..."`; that file is excluded by `.gitignore`.

Then launch:

```bash
streamlit run app.py
```

Open the local address printed by Streamlit, usually `http://localhost:8501`. Without a key, the app still works with scripted hints.

## Test

Activate the virtual environment and run:

```bash
python -m pytest -q
```

The tests cover exercise definitions, hint levels, request context, missing keys, mocked API errors, response-leak safeguards, code retention, progression and Solo Check restrictions. Pytest makes no paid API requests.

Phase 4 verification: the scripted-only `AppTest` journey passed through all three
exercises, hint requests, code revisions, dashboard, and restart. The full suite
passed **33 tests**; mypy reported no issues in six application modules, and
`compileall` completed successfully. This was automated acceptance testing, not a
participant usability study.

### Evaluator refinement

Manual testing reported that a correct Solo Check solution with an explicit `else`
was rejected because the original checker required the entire submitted AST to
exactly match one reference AST. The evaluator now recognizes bounded patterns for
the three exercises: direct or simple-alias average calculations; equivalent
remainder comparisons for evenness; and conditional, inline-conditional, or
`max`-based selection of the larger input. It distinguishes syntax errors,
recognizable incorrect logic, and valid structures it cannot safely check.

The regression suite now passes **42 tests**; mypy reports no issues in six
application modules, and Python compilation succeeds. This improves feedback
accuracy for supported alternatives, but it does not prove complete behavioral
equivalence. Supported patterns and the manual finding are recorded in
`docs/development_record.md`.

## Development record

- Phase 1: Streamlit shell and project setup.
- Phase 2: exercises, scripted progressive hints, safe structural validation, progression, Solo Check and session summary.
- Phase 3: contextual OpenAI Responses API hints, request-only calls, session hint caching, fallback and response checks. Static SDK/model documentation and mocked tests were verified; live account/model access was not verified because no API key was configured.
- Phase 4: end-to-end offline acceptance test, explicit hint-mode and progression guidance, scripted-only safeguard, usability plan and storyboard materials. No participant study or learning outcome is claimed.
- Later work may include explain-back questions, adaptive hint fading and long-term analytics.

The repository is connected to GitHub. Phase 4 working-tree changes are local and have not been pushed. No participant study or learning outcome is claimed.

## Offline evaluation and storyboards

To guarantee that no hint request reaches OpenAI—even if a key exists in your environment or Streamlit secrets—start the app in scripted-only mode:

```bash
SOCRATICCODE_SCRIPTED_ONLY=1 streamlit run app.py
```

The interface labels this mode and uses the scripted hints. It does not modify or delete saved credentials. Follow [docs/usability-evaluation.md](docs/usability-evaluation.md) to conduct three participant sessions and record results without inventing findings. [docs/storyboards.md](docs/storyboards.md) gives three reproducible screenshot scenarios.

## AI assistance

AI coding assistance was used in the VS Code Copilot environment. Suggestions were checked against the requirements, automated tests and local Streamlit startup. No live model response or user-testing result is claimed.
