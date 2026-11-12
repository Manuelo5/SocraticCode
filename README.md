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

Edit `.env` locally and set `OPENAI_API_KEY` to your own key. The `-n` option leaves an existing `.env` unchanged; edit your existing file if you already have one. Do not commit `.env` or paste the key into chat. API use may incur charges. `OPENAI_MODEL` defaults to `gpt-6-luna` and can be changed to another model available to your API account. Alternatively, configure `OPENAI_API_KEY` in `.streamlit/secrets.toml` as `OPENAI_API_KEY = "..."`; that file is excluded by `.gitignore`.

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
- Phase 3: contextual OpenAI Responses API hints, request-only calls, session hint caching, fallback and response checks.
- Later work may include explain-back questions, adaptive hint fading and long-term analytics.

The local Phase 3 work is prepared in Git but has not been pushed to GitHub. No usability study or learning outcome is claimed.

## AI assistance

AI coding assistance was used in the VS Code Copilot environment. Suggestions were checked against the requirements, automated tests and local Streamlit startup. No live model response or user-testing result is claimed.
