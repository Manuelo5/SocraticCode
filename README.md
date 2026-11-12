README prose word count: approximately 600 words.

# SocraticCode — An AI Tutor That Teaches You to Think

SocraticCode is a local Streamlit app for beginner Python debugging. Two guided exercises use context-aware AI hints when an OpenAI API key is configured; a four-level scripted hint ladder is used if the key is missing or the API response is unavailable or withheld. Exercise 3 is an independent Solo Check with all hint controls disabled.

## What works

- Three editable debugging tasks: calculate an average, check whether a number is even, and return the larger of two numbers.
- Students request one hint at a time. The tutor sees the current exercise, learning objective, current code, requested level and earlier hints.
- AI output is labelled AI-generated. Missing credentials, API failures, empty responses, oversized responses and detected full-solution leaks use a clearly labelled scripted fallback.
- One hint result is cached per exercise and level in the current Streamlit session. Ordinary reruns do not make model requests.
- Only an explicit guided-hint request sends the current exercise code and minimal exercise context to OpenAI; no personal information is added.
- The first two exercises must be completed before the Solo Check unlocks. The Solo Check has no AI hints, scripted hints or chat.
- Progress, code drafts, hint history, submissions and Solo Check outcome are stored in session state.
- The evaluator parses and structurally compares the target function's AST. It never executes student code.

## Limitations

Prompt instructions and output checks reduce the chance of a complete solution leak but cannot guarantee the model will never reveal one. The local safeguard detects verbatim solution text and syntax-equivalent functions in code blocks; it cannot detect every semantically equivalent answer. Structural AST comparison is not behavioral testing and can reject another correct implementation. Progress is session-only. Live AI behavior was not tested during development; automated API tests use mocks.

## Phase 3 verification status

The installed OpenAI Python SDK is version 3.49.0, and the Responses API call shape was checked against the installed SDK. OpenAI's current [GPT-6 Luna model documentation](https://developers.openai.com/api/docs/models/gpt-6-luna) lists the Responses endpoint as supported. This does not confirm that the model is enabled for your API account. No valid key was configured during verification, so account access and live AI hints could not be tested. The local `.env` was created from `.env.example` and still contains only its placeholder.

The complete mocked/offline test suite passed **32 tests**. It covers AI request parameters, fallback behavior, hint caching and code preservation, and Solo Check restrictions. No live or billable API calls were made. Verification also caught and fixed a configuration edge case: the example `your_api_key_here` value is now treated as missing, so it cannot trigger an API request.

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

## Development record

- Phase 1: Streamlit shell and project setup.
- Phase 2: exercises, scripted progressive hints, safe structural validation, progression, Solo Check and session summary.
- Phase 3: contextual OpenAI Responses API hints, request-only calls, session hint caching, fallback and response checks. Static SDK/model documentation and mocked tests were verified; live account/model access was not verified because no API key was configured.
- Later work may include explain-back questions, adaptive hint fading and long-term analytics.

The local Phase 3 work is prepared in Git but has not been pushed to GitHub. No usability study or learning outcome is claimed.

## AI assistance

AI coding assistance was used in the VS Code Copilot environment. Suggestions were checked against the requirements, automated tests and local Streamlit startup. No live model response or user-testing result is claimed.
