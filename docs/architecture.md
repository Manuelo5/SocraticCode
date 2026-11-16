# SocraticCode architecture

The diagram distinguishes implemented prototype and Phase 4 evaluation support from
the unverified live AI path and optional future work.

```mermaid
flowchart LR
    Student[Student]
    UI[Streamlit interface<br/>Implemented]
    Controller[Hint controller<br/>Implemented: deterministic levels 1–4]
    Tutor[AI tutor<br/>Implemented adapter; live behavior unverified]
    API[OpenAI API<br/>Requires configured key and account access]
    Fallback[Scripted hint fallback<br/>Implemented]
    Offline[Scripted-only evaluation mode<br/>Implemented; bypasses credentials]
    Evaluator[Code evaluator<br/>Implemented: AST structure comparison; no execution]
    Progress[Progress tracker<br/>Implemented: Streamlit session state]
    Planned[Optional planned work<br/>Explain-back prompts, adaptive hint fading,<br/>long-term analytics and instructor tools]

    Student --> UI
    UI -->|explicit hint request, guided exercises only| Controller
    Controller -->|scripted-only mode| Offline
    Offline --> Fallback
    Controller -->|key configured| Tutor
    Tutor -->|Responses API request| API
    API -->|bounded text response| Tutor
    Tutor -->|safe response| UI
    Tutor -->|missing key, API error, empty or unsafe response| Fallback
    Fallback --> UI
    UI -->|submit code| Evaluator
    Evaluator -->|correctness feedback| UI
    UI <--> Progress
    Student -->|edit code| UI
    Planned -. future .-> UI
```

## Implemented boundaries

- The hint controller advances exactly one level per request and refuses hints for the Solo Check.
- The AI tutor receives the exercise objective, current student code, hint level and earlier hints. It does not receive the reference solution.
- The OpenAI client has a 20-second timeout, automatic retries disabled, a conservative output-token cap and response storage disabled. A model call occurs only after an explicit hint-button request.
- `SOCRATICCODE_SCRIPTED_ONLY=1` bypasses environment and Streamlit credentials, allowing safe scripted evaluation without changing saved keys.
- Hints are cached per exercise/level for the current session. API errors or a detected full-solution response produce a visible scripted fallback.
- API keys are read from `OPENAI_API_KEY` in the environment or Streamlit secrets. Local `.env` and `.streamlit/secrets.toml` files are ignored by Git.
- The evaluator parses and compares syntax trees and never executes untrusted student code.
- The Solo Check has no tutor entry point or hint widget.
- The Phase 4 acceptance journey is automated with Streamlit `AppTest`; participant evaluation materials are prepared but no participant sessions have been conducted.

## Known limitations and planned components

Prompt instructions and output checks reduce, but cannot eliminate, solution leakage. The structural evaluator may reject a logically correct implementation with different syntax. Progress is not persisted between sessions. Optional explain-back prompts, adaptive assistance fading, long-term performance analytics and instructor dashboards are not implemented.
